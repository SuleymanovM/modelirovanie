import csv
from modeli3 import lab4_import
import math
import numpy as np
import matplotlib.pyplot as plt


class CsvOut:
    request_number: int
    message_type: int
    moment_of_appearance: float
    moment_of_service_start: float
    waiting_time: float
    time_spent: float
    time_service: float

    def __init__(self, request_number, message_type, moment_of_appearance, moment_of_service_start, waiting_time, time_spent, time_service):
        self.request_number = request_number
        self.message_type = message_type
        self.moment_of_appearance = moment_of_appearance
        self.moment_of_service_start = moment_of_service_start
        self.waiting_time = waiting_time
        self.time_spent = time_spent
        self.time_service = time_service


class Message:
    number: int
    type: str
    destination: int
    length: int
    time: float
    moment_of_appearance: float

    def __init__(self, number, type, destination, length, time, moment_of_appearance=0):
        self.number = number
        self.type = str(type)
        self.destination = destination
        self.length = length
        self.time = time
        self.moment_of_appearance = moment_of_appearance

    def entrance(self, main_time):
        return self.time < main_time


def channel_emulating(data, channel_speed, is_priority):
    query = [data[0]]
    query[0].moment_of_appearance = data[0].time
    data.pop(0)
    main_time = 0.0
    table = []

    while query:
        if is_priority:
            query = sorted(query, key=lambda x: (x.type, x.number))

        moment_time = 0

        if main_time < query[0].time:
            main_time = query[0].time

        moment_time += query[0].length / channel_speed
        table.append(CsvOut(query[0].number, query[0].type, query[0].time, main_time, main_time - query[0].time,
                            main_time - query[0].time + moment_time, moment_time))
        main_time += moment_time

        query.pop(0)

        k = 0
        for msg in data:
            if msg.time <= main_time:
                k += 1
                query.append(msg)
            elif not query:
                k += 1
                query.append(msg)
                break

        for _ in range(k):
            data.pop(0)

    return table


def characteristics(table1, table2, keys):
    table = table1 + table2
    time1_1, time1_2, time2_1, time2_2 = 0, 0, 0, 0

    d = {key: [] for key in keys}
    keys2 = ['R', 'JL', 'W', 'L', 'U']
    d2 = {key: [] for key in keys2}
    u, D, σ, μ, λ, ρ, η, w, ri, un = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]
    u_len = [1, 1, 1]
    r = [[], [], []]
    k = 0
    for elem in table:
        k += 1
        if elem.waiting_time != 0:
            k += 1
        if elem.message_type == '1':
            u[0] += elem.time_spent - elem.waiting_time
            u_len[0] += 1
            D[0] += elem.waiting_time ** 2
            w[0] += elem.waiting_time
            r[0].append(elem.moment_of_appearance)

        if elem.message_type == '2':
            u[1] += elem.time_spent - elem.waiting_time
            u_len[1] += 1
            D[1] += elem.waiting_time ** 2
            w[1] += elem.waiting_time
            r[1].append(elem.moment_of_appearance)

        if elem.message_type == '3':
            u[2] += elem.time_spent - elem.waiting_time
            u_len[2] += 1
            D[2] += elem.waiting_time ** 2
            w[2] += elem.waiting_time
            r[2].append(elem.moment_of_appearance)

        if elem.message_type == '4':
            u[3] += elem.time_spent - elem.waiting_time
            u_len[3] += 1
            D[3] += elem.waiting_time ** 2
            w[3] += elem.waiting_time
            r[3].append(elem.moment_of_appearance)

    for i in table1:
        time1_1 += i.moment_of_service_start
        time1_2 += i.moment_of_appearance
    for i in table2:
        time2_1 += i.moment_of_service_start
        time2_2 += i.moment_of_appearance

    for i in range(len(r)):
        for j in range(len(r[i]) - 1):
            r[i] = r[i][::-1]
            r[i][j] = r[i][j] - r[i][j + 1]
        if len(r[i]) != 0:
            ri[i] = sum(r[i]) / len(r[i])
        else:
            ri[i] = 0
    for i in range(len(u)):
        u[i] = u[i] / u_len[i] #среднее время обслуживания заявки i-го типа;
        print((u[i]))
        print((u_len[i]))
        un[i] = u[i] ** 2 #второй начальный момент времени обслуживания
        D[i] = D[i] / u_len[i] #дисперсия времени обслуживания
        σ[i] = math.sqrt(D[i]) #среднеквадратичное отклонение времени обслуживания
        μ[i] = u_len[i] / (time2_1 + time2_2) #интенсивность обслуживания
        λ[i] = u_len[i] / (time1_1 + time1_1) #– среднее число заявок, поступающих на обслуживание
        ρ[i] = λ[i] / μ[i] # коэффициент загрузки оборудования заявками i-го типа;
        η[i] = 1 - ρ[i] #коэффициент простоя
        w[i] = w[i] / u_len[i] #среднее время пребывания заявки i-го типа в очереди

    d['u'] = u
    d['un'] = un
    d['D'] = D
    d['σ'] = σ
    d['μ'] = μ
    d['λ'] = λ
    d['ρ'] = ρ
    d['η'] = η
    d['w'] = w
    d['r'] = ri
    d2['R'] = sum(d['ρ'])
    d2['JL'] = sum(d['λ'])
    d2['W'] = sum(d['w'])
    d2['L'] = k / sum(u_len)
    U = 0
    for i in table:
        U += i.time_spent
    d2['U'] = U / len(table)
    return d, d2


# Задаем скорость передачи информации (V символов/с)
channel_speed = 100

data = lab4_import()
message_data = []
for num, _ in enumerate(data, start=1):
    message_data.append(Message(num, _[0], _[1], _[2], _[3]))

data_for2 = message_data.copy()
data_for3 = message_data.copy()
table1 = channel_emulating(message_data, channel_speed, False)

# Открываем файл для записи
with open('lab4_output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Номер заявки", "Тип сообщения", "Момент появления", "Момент начала обслуживания", "Время ожидания",
                  "Время пребывания в канале", 'Время обслуживания']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for item in table1:
        writer.writerow({
            "Номер заявки": item.request_number,
            "Тип сообщения": item.message_type,
            "Момент появления": np.round(item.moment_of_appearance, 3),
            "Момент начала обслуживания": np.round(item.moment_of_service_start, 3),
            "Время ожидания": np.round(item.waiting_time, 3),
            "Время пребывания в канале": np.round(item.time_spent, 3),
            "Время обслуживания": np.round(item.time_service, 3)
        })

print("Данные записаны в lab4_output.csv")

table2 = channel_emulating(data_for2, channel_speed, True)
with open('lab4_output2.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["Номер заявки", "Тип сообщения", "Момент появления", "Момент начала обслуживания", "Время ожидания",
                  "Время пребывания в канале", 'Время обслуживания']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for item in table2:
        writer.writerow({
            "Номер заявки": item.request_number,
            "Тип сообщения": item.message_type,
            "Момент появления": np.round(item.moment_of_appearance, 3),
            "Момент начала обслуживания": np.round(item.moment_of_service_start, 3),
            "Время ожидания": np.round(item.waiting_time, 3),
            "Время пребывания в канале": np.round(item.time_spent, 3),
            "Время обслуживания": np.round(item.time_service, 3)
        })

print("Данные записаны в lab4_output2.csv")
keys = ['u', 'un', 'D', 'σ', 'μ', 'λ', 'ρ', 'η', 'w', 'r']
d1, d2 = characteristics(table1, table2, keys)

with open('lab4_output3.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    writer.writerow(keys)

    # Запись значений
    for i in range(3):
        row = [np.round(d1[key][i], 4) for key in keys]
        writer.writerow(row)

print("Данные записаны в lab4_output3.csv")
print(d2)

u, r, w = [[], [], []], [[], [], []], [[], [], []]
R, W, U, L = [], [], [], []

for i in range(1, 11):
    data_for = data_for3.copy()
    mas = channel_emulating(data_for, 10 * i, False)
    d1, d2 = characteristics(mas, mas, keys)
    for i in range(len(d1['u'])):
        u[i].append(d1['u'][i])
        r[i].append(d1['r'][i])
        w[i].append(d1['w'][i])
    R.append(d2['R'])
    W.append(d2['W'])
    U.append(d2['U'])
    L.append(d2['L'])

x = [10 * i for i in range(1, 11)]

# Графики для u
fig, axes = plt.subplots(1, len(u), figsize=(20, 5))
for i in range(len(u)):
    axes[i].plot(x, u[i])
    axes[i].set_xlabel('скорость')
    axes[i].set_ylabel('время обслуживания')
    axes[i].set_title(f'u_i(V) для типа сообщения {i + 1}')
plt.tight_layout()
plt.show()

# Графики для r
fig, axes = plt.subplots(1, len(u), figsize=(20, 5))
for i in range(len(r)):
    axes[i].plot(x, r[i])
    axes[i].set_xlabel('скорость')
    axes[i].set_ylabel('промежуток поступления')
    axes[i].set_title(f'r_i(V) для типа сообщения {i + 1}')
plt.tight_layout()
plt.show()

# Графики для w
fig, axes = plt.subplots(1, len(u), figsize=(20, 5))
for i in range(len(u)):
    axes[i].plot(x, w[i])
    axes[i].set_xlabel('скорость')
    axes[i].set_ylabel('время пребывания')
    axes[i].set_title(f'w_i(V) для типа сообщения {i + 1}')
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(2, 2, figsize=(10, 10))
# График для U
axes[0, 0].plot(x, U)
axes[0, 0].set_xlabel('скорость')
axes[0, 0].set_ylabel('время заявки в системе')
axes[0, 0].set_title('U(V)')

# График для R
axes[0, 1].plot(x, R)
axes[0, 1].set_xlabel('скорость')
axes[0, 1].set_ylabel('коэффициент загрузки')
axes[0, 1].set_title('R(V)')

# График для W
axes[1, 0].plot(x, W)
axes[1, 0].set_xlabel('скорость')
axes[1, 0].set_ylabel('время заявки в очереди')
axes[1, 0].set_title('W(V)')

# График для L
axes[1, 1].plot(x, L)
axes[1, 1].set_xlabel('скорость')
axes[1, 1].set_ylabel('число заявок в системе')
axes[1, 1].set_title('L(V)')
plt.tight_layout()
plt.show()