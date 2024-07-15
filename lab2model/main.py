import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

def generate_poisson_table_based(lambda_value, max_value, sample_size):#генерировать Пуассонову таблицу на основе параметров
    # списки для хранения данных
    values = []
    xi_values = []
    table = []
    cumulative_probabilities = []

    # Создание таблицы вероятностей от 0 до 84
    for x in range(max_value + 1):
        xi_values.append(x)#Каждое значение x от 0 до max_value добавляется в список xi_values
        poisson_prob = (math.exp(-lambda_value) * lambda_value ** x) / math.factorial(x)#для каждого числа х вычисляется вероятность
        table.append((poisson_prob, x))#добавляется в таблицу table вместе со значением x
        cumulative_probabilities.append(sum(prob for prob, _ in table))#сумма вероятностей для каждого значения x в таблице вычисляется
        # и добавляется в список cumulative_probabilities.

    # Генерация случайных чисел с использованием табличного метода
    for _ in range(sample_size):
        r = random.uniform(0, 1)
        x = None #Устанавливаем начальное значение x (неопределенное)

        for i in range(len(cumulative_probabilities)):
            #находится ли случайное число r между двумя значениями вероятностей cumulative_probabilities[i-1] и cumulative_probabilities[i]. Если это условие выполняется,
            # то значит мы найдем интервал, в котором находится случайное число r.
            if cumulative_probabilities[i-1] < r <= cumulative_probabilities[i]:
                x_min = xi_values[i-1]
                x_max = xi_values[i]
                f_x_min = cumulative_probabilities[i-1]
                f_x_max = cumulative_probabilities[i]
                #С помощью линейной интерполяции вычисляем значение x, которое попадает в интервал, используя формулу
                x = round(x_min + ((r - f_x_min) / (f_x_max - f_x_min)) * (x_max - x_min))
                break
#После нахождения значения x мы добавляем его в список values.
        values.append(x)

    return values #Возвращаем список сгенерированных значений values.

def calculate_poisson_characteristics(values):
    sample_size = len(values)
    mean = sum(values) / sample_size
    variance = sum((x - mean) ** 2 for x in values) / sample_size
    standard_deviation = math.sqrt(variance)

    return mean, variance, standard_deviation


lambda_value = 28
max_value = 84
sample_size = 100
#для генерации Пуассоновой таблицы и сохранения результата в переменной values
values = generate_poisson_table_based(lambda_value, max_value, sample_size)

# Округление до целых значений
values = [int(x) for x in values]

# Вычисление характеристик
mean, variance, standard_deviation = calculate_poisson_characteristics(values)


# Вывод результатов
print("Случайно сгенерированные целые числа:")
print(values)
print()
print("Математическое ожидание (М):", mean)
print("Дисперсия (D):", variance)
print("Среднеквадратичное отклонение (SD):", standard_deviation)

# Построение графика функции плотности вероятностей
x = np.arange(0, 100)
plt.plot(x, poisson.pmf(x, lambda_value), 'o-', label='f(X)')
plt.title('Функция плотности вероятностей')
plt.xlabel('X')
plt.ylabel('P(X)')
plt.show()

# Построение графика функции распределения вероятностей
x = np.arange(0, 100)
plt.plot(x, poisson.cdf(x, lambda_value), 'o-', label='F(X)')
plt.title('Функция распределения вероятностей')
plt.xlabel('X')
plt.ylabel('P(X <= x)')
plt.show()