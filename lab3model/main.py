import time
import numpy as np
import pandas as pd

MESSAGES_QUANTITY = 100
TYPES = [1, 2, 3]
# Вероятности появления типов сообщений
PROBABILITIES = [0.01, 0.71, 0.28]
RECIPIENTS = [1, 2, 3, 4, 5]
# Вероятности получения сообщений разными получателями для каждого типа сообщения
RECIPIENTS_PROBABILITIES = {
    1: [0.74, 0.02, 0.03, 0.2, 0.01],
    2: [0.2, 0.07, 0.4, 0.26, 0.07],
    3: [0.68, 0.1, 0, 0.15, 0.07],
}
a, b = 2, 1.9

previous_timestamp = 0

# Генерирует случайное время на основе распределения Вейбулла с параметрами a и b.
def get_time():
    global previous_timestamp
    interval = 0.22791218757629395  # Fixed time interval between messages
    current_timestamp = previous_timestamp + interval
    previous_timestamp = current_timestamp
    return current_timestamp


class Message:
    ms_type: int
    recipient: int
    recipient_probabilities: list
    message_len: int
    timestamp: int | float

#Инициализация сообщения.
    def __init__(self, message_type):
        self.ms_type = message_type
        self.recipient_probabilities = RECIPIENTS_PROBABILITIES[self.ms_type]
        self.recipient = np.random.choice(RECIPIENTS, p=self.recipient_probabilities)
        self.message_len = np.random.randint(21, 194)
        self.timestamp = get_time()

    def __str__(self):
        return (f"message_type: {self.ms_type}, recipient: {self.recipient}, "
                f"length: {self.message_len}, timestamp: {self.timestamp}")

    def dict(self):
        return {"message_type": self.ms_type, "recipient": self.recipient,
                "length": self.message_len, "timestamp": self.timestamp}

#представляет группу сообщений и выполняет анализ этой группы.
class MessageFlow:
    messages: list[Message]
    parsed_messages = {"types": [], "lengths": [], "recipients": []}
    type_stats: list

#инициализация объекта
    def __init__(self, messages: list[Message]):
        self.messages = messages
        self.parse_messages()
        self.type_stats = self.calculate_type_stats()

#парсинг атрибутов из сообщений
    def parse_messages(self):
        for i in self.messages:
            self.parsed_messages["types"].append(i.ms_type)
            self.parsed_messages["lengths"].append(i.message_len)
            self.parsed_messages["recipients"].append(i.recipient)

#Вычисляет статистику по типам сообщений.
    def calculate_type_stats(self):
        res = []
        all_recipients = []
        for ms_type in TYPES:
            count = 0
            lengths = []
            recipients = []
            for message in self.messages:
                if message.ms_type == ms_type:
                    count += 1
                    lengths.append(message.message_len)
                    recipients.append(message.recipient)
                    all_recipients.append(message.recipient)
            res.append({"Тип": ms_type,
                        "Кол-во": count,
                        "Вероятность появления": count / 100,
                        "Средняя длина": sum(lengths) / count if count != 0 else 0,
                        "Максимальная длина": max(lengths) if count != 0 else 0,
                        "Теоретическая длина": PROBABILITIES[ms_type - 1] * 100,
                        "Теоретическая вероятность": PROBABILITIES[ms_type - 1], }
                       )
            for i in RECIPIENTS:
                res[-1].update({f"Получатель {i}": recipients.count(i) / count if count != 0 else 0,
                                f"Теоретически {i}": RECIPIENTS_PROBABILITIES[ms_type][i - 1]})

        return res

    #преобразование сообщений в список словарей
    def unpack(self):
        return sorted(list(map(lambda x: x.dict(), self.messages)), key=lambda x: x['timestamp'])

    def to_excel(self, filename: str):
        data = self.unpack()
        print(data)
        data[0].update({"": ""})
        for i in range(len(self.type_stats)):
            data[i].update(self.type_stats[i])
        df = pd.DataFrame(data)

        excel_filename = filename
        df.to_excel(excel_filename, index=False, engine='openpyxl')

#
def get_list_of_messages():
    return list(map(Message, np.random.choice(TYPES, size=MESSAGES_QUANTITY, p=PROBABILITIES)))


if __name__ == '__main__':
    messages = get_list_of_messages()
    messages_flow = MessageFlow(messages)
    messages_flow.to_excel(filename='output_data.xlsx')


