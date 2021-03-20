"""

Работа с csv файлами.
Импорт и экспорт данных.

Обрабатываются файлы с содержимым, вида:
<date>,<name>,<temperature>
<date>,<name>,<temperature>
<date>,<name>,<temperature>
...

"""

import csv
from datetime import datetime
from typing import List

from database import ThermometryLog, Float
from logger import logger


def import_data(filename: str, database: ThermometryLog):
    """
    Импортируем данные из csv файла.
    :param filename: Имя файла.
    :param database: API для работы с базой данных.
    """

    logger.info("Импорт записей.")
    with open(filename, encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # Валидация полей
            if len(name := row[1]) == 0:
                continue
            try:
                date = datetime.strptime(row[0], "%d.%m.%Y")
                temperature = float(row[2])
            except ValueError:
                continue

            database.insert(
                name=name,
                temperature=Float(round(temperature, 1)),
                date=date.strftime("%d.%m.%Y"),
            )


def export_data(filename: str, dates: List[str], database: ThermometryLog):
    """
    Экспортируем данные в csv файл.
    :param filename: Имя файла.
    :param dates: Даты, которые нужно экспортировать (в формате '%d.%m.%Y').
    :param database: API для работы с базой данных.
    """

    logger.info("Заполнение файла.")
    with open(filename, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for date in dates:
            data: List[ThermometryLog] = database.filter(return_list=True, date=date)
            if len(data):
                for obj in data:
                    writer.writerow([obj.date, obj.name, obj.temperature])
