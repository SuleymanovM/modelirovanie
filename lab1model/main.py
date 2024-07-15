import random
class CellularAutomaton:
    def __init__(self, seed, rule):
        self.seed = seed
        self.rule = rule

    def extract_number(self):
        # Преобразование
        #   в двоичный код и добавление ведущего нуля
        binary_seed = bin(self.seed)[2:].zfill(32)
        # Генерация следующего значения
        next_seed = int(binary_seed[1:] + binary_seed[0], 2)
        self.seed = next_seed
        # Преобразование правила в двоичный код и разворот битов
        binary_seed_after_rule = bin(self.rule)[2:].zfill(8)
        # Получение нового бита из правила на основе последнего бита семени
        binary_seed_after_rule = binary_seed_after_rule[::-1]

        new_bit = binary_seed_after_rule[int(binary_seed[-1])]
        # Генерация следующего случайного числа и возвращение его
        next_seed = (next_seed << 1) | int(new_bit)

        return next_seed % 1000

# Генерация случайных чисел с помощью стандартного генератора
count1 = 100
count2 = 1000
count3 = 10000

print()
print("Задание 1 \n Стандартный генератор")
random_num = []
for _ in range(count1):
    random_num.append(round(random.random() * 1000))
M = sum(random_num) / len(random_num)
D = sum((x - M) ** 2 for x in random_num) / count1
O = D ** 0.5
print()
print("N = 100 ")
print("Выборка ", random_num)
print("Мат. ожидание ", M)
print("Дисперсия ", D)
print("Среднеквадратичное отклонение ", O)

random_num = []
for _ in range(count2):
    random_num.append(round(random.random() * 1000))
M = sum(random_num) / len(random_num)
D = sum((x - M) ** 2 for x in random_num) / count2
O = D ** 0.5
print()
print("N = 1000 ")
print("Выборка ", random_num)
print("Мат. ожидание ", M)
print("Дисперсия ", D)
print("Среднеквадратичное отклонение ", O)

random_num = []
for _ in range(count3):
    random_num.append(round(random.random() * 1000))
M = sum(random_num) / len(random_num)
D = sum((x - M) ** 2 for x in random_num) / count3
O = D ** 0.5
print()
print("N = 10000 ")
print("Выборка ", random_num)
print("Мат. ожидание ", M)
print("Дисперсия ", D)
print("Среднеквадратичное отклонение ", O)

# Генерация случайных чисел
# с помощью генератора на базе клеточного автомата
print()
print("Задание 2 \n Генератор на базе клеточного автомата")
seed = 12
rule = 30
automaton = CellularAutomaton(seed, rule)
random_num = []

for _ in range(count1):
    random_number1 = automaton.extract_number()
    random_num.append(random_number1)

M = sum(random_num) / len(random_num)
D = sum((x - M) ** 2 for x in random_num) / count1
O = D ** 0.5
print()
print("N = 100 ")
print("Выборка ", random_num)
print("Мат. ожидание ", M)
print("Дисперсия ", D)
print("Среднеквадратичное отклонение ", O)

seed = 1236
rule = 110
automaton = CellularAutomaton(seed, rule)
random_num = []

for _ in range(count2):
    random_number1 = automaton.extract_number()
    random_num.append(random_number1)

M = sum(random_num) / len(random_num)
D = sum((x - M) ** 2 for x in random_num) / count2
O = D ** 0.5
print()
print("N = 1000 ")
print("Выборка ", random_num)
print("Мат. ожидание ", M)
print("Дисперсия ", D)
print("Среднеквадратичное отклонение ", O)

seed = 1238
rule = 45
automaton = CellularAutomaton(seed, rule)
random_num = []

for _ in range(count3):
    random_number1 = automaton.extract_number()
    random_num.append(random_number1)

#(D) вычисляется как сумма квадратов разности между каждым числом (x) в списке случайных чисел (random_num) и средним значением (M),
# деленная на количество чисел в списке (len(random_num))

M = sum(random_num) / len(random_num)
D = sum((x - M) ** 2 for x in random_num) / count3
O = D ** 0.5
print()
print("N = 10000 ")
print("Выборка ", random_num)
print("Мат. ожидание ", M)
print("Дисперсия ", D)
print("Среднеквадратичное отклонение ", O)