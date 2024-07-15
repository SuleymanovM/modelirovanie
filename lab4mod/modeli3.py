import csv
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from scipy.stats import gamma


def task_1(probability, count):
    F_table = [0]
    for x in range(len(probability)):
        F = F_table[x] + probability[x]
        F_table.append(F)

    random_numbers = []
    for _ in range(count):
        r = np.random.random()

        # Используем метод последовательного сравнения для нахождения интервала
        for i in range(1, len(F_table)):
            if F_table[i - 1] < r <= F_table[i]:
                F_prev = F_table[i - 1]
                F_curr = F_table[i]
                # Используем метод линейной интерполяции для вычисления случайного числа X
                X = i + ((r - F_prev) / (F_curr - F_prev)) * (i - (i - 1))
                random_numbers.append(int(X))
                break
    return random_numbers


def task_2(probability, start_random_numbers):
    random_numbers = []

    F_table = [[0] for _ in range(len(probability))]
    for x in range(len(probability)):
        F = 0
        for i in range(len(probability[x])):
            F += probability[x][i]
            F_table[x].append(F)

    for _ in start_random_numbers:
        r = np.random.random()
        if r <= F_table[_ - 1][1]:
            random_numbers.append(1)
            continue

        if r <= F_table[_ - 1][2]:
            random_numbers.append(2)
            continue

        if r <= F_table[_ - 1][3]:
            random_numbers.append(3)
            continue

        if r <= F_table[_ - 1][4]:
            random_numbers.append(4)
            continue

        if r <= F_table[_ - 1][5]:
            random_numbers.append(5)
            continue

    return random_numbers


def task_3(a, b, random_task_1):
    random_numbers = []

    for _ in random_task_1:
        random_numbers.append(random.randint(a, b))

    return random_numbers


def task_4(mean, zorlang, num_samples):
    # Вычисляем параметры распределения Эрланга
    k = (mean / zorlang) ** 2
    beta = mean / k

    # Генерируем случайные числа с распределением Эрланга
    random_numbers = gamma.rvs(a=k, scale=1/beta, size=num_samples)

    return random_numbers
def lab4_import():
    probability_task1 = [0.51, 0.02, 0.47]
    probability_task2 = [[0.49, 0.05, 0.22, 0.06, 0.18],
                         [0.62, 0.2, 0.01, 0.11, 0.06],
                         [0.56, 0.27, 0.02, 0.14, 0.01]]
    count = 100

    random_task_1 = task_1(probability_task1, count)
    print('Генерация типов сообщения:')
    for i, num in enumerate(random_task_1, start=1):
        print(num, end=' ')
        if i % 10 == 0:
            print()

    data_cnt = Counter(random_task_1)
    data = [data_cnt[elem] for elem in data_cnt]
    print(f"\nТип 1: {data_cnt[1]}\nТип 2: {data_cnt[2]}\nТип 3: {data_cnt[3]}\n")

    random_task_2 = task_2(probability_task2, random_task_1)
    for i, num in enumerate(random_task_2, start=1):
        print(num, end=' ')
        if i % 10 == 0:
            print()

    data_cnt = Counter(random_task_2)
    data = [data_cnt[elem] for elem in data_cnt]
    print(f"\nАдрес 1: {data_cnt[1]}\nАдрес 2: {data_cnt[2]}\nАдрес 3: {data_cnt[3]}\nАдрес 4: {data_cnt[4]}\nАдрес 5: {data_cnt[5]}\n")

    a = 4
    b = 122


    random_task_3 = task_3(a, b, random_task_1)

    for i, num in enumerate(random_task_3, start=1):
        print(num, end=' ')
        if i % 10 == 0:
            print()
    print(f'Средняя длинна сообщений: {sum(random_task_3)/len(random_task_3)}')

    mean = 1.9
    zorlang = 1.0

    print('Генерация времени:')
    random_task_4 = task_4(mean, zorlang, count)
    for i, num in enumerate(random_task_4, start=1):
        print("{:.3f}".format(num), end=' ')
        if i % 10 == 0:
            print()

    random_task_4_final = [random_task_4[0]]
    for i in range(1, len(random_task_4)):
        random_task_4_final.append(random_task_4[i])


    # Создаем список, в котором каждый элемент - это кортеж из значений для каждого столбца
    data = list(zip(random_task_1, random_task_2, random_task_3, random_task_4_final))

    # Укажите имя файла, в который вы хотите сохранить таблицу
    output_file = "lab3_output.csv"

    # Создаем и записываем данные в CSV-файл
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Записываем заголовок таблицы
        writer.writerow(["Тип сообщения", "Адрес абонента", "Длина сообщения", "Время поступления сообщения"])

        # Записываем данные из массивов
        writer.writerows(data)

    cont = [0, 0, 0]
    for _ in random_task_1:
        if _ == 1:
            cont[0] += 1
        if _ == 2:
            cont[1] += 1
        if _ == 3:
            cont[2] += 1
    for i in range(len(cont)):
        print(f"заявок типа {i + 1}: {cont[i]/len(random_task_1)} ")
    return data
