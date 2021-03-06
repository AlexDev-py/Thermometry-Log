"""

Работа с csv файлами.
Импорт и экспорт данных.

Обрабатываются файлы с содержимым, вида:
<date>,<arrival_time>,<leaving_time>,<name>,<temperature>
<date>,<arrival_time>,<leaving_time>,<name>,<temperature>
<date>,<arrival_time>,<leaving_time>,<name>,<temperature>
...

"""

import csv
from datetime import datetime
from typing import List

from database import ThermometryLog, Float
from logger import logger


def import_data(filename: str, database: ThermometryLog, date: str, group: int = 0):
    """
    Импортирует данные из csv файла.
    :param filename: Имя файла.
    :param database: API для работы с базой данных.
    :param date: Дата, на которую импортируется шаблон (В формате '%Y-%m-%d').
    :param group: Группа, в которую импортируем данные.
    """

    logger.info("Импорт записей.")
    date = datetime.strptime(date, "%Y-%m-%d")
    with open(filename, encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # Валидация полей
            if len(name := row[3]) == 0:
                continue
            try:
                if row[0] != "<TODAY>":  # Замена шаблона
                    date = datetime.strptime(row[0], "%d.%m.%Y")
                temperature = 0 if row[4] == "<NONE>" else float(row[4])
                arrival_time = 0 if row[1] == "<NONE>" else row[1]
                leaving_time = 0 if row[2] == "<NONE>" else row[2]
            except ValueError:
                continue

            database.insert(
                need_commit=False,
                name=name,
                temperature=Float(round(temperature, 1)),
                date=date.strftime("%d.%m.%Y"),
                grp=group,
                arrival_time=arrival_time,
                leaving_time=leaving_time,
            )
    database.commit()


def export_data(
    filename: str,
    dates: List[str],
    database: ThermometryLog,
    group: int = 0,
    template=False,
):
    """
    Экспортирует данные в csv файл.
    :param filename: Имя файла.
    :param dates: Даты, которые нужно экспортировать (в формате '%d.%m.%Y').
    :param database: API для работы с базой данных.
    :param group: Группа из которой импортируем данные.
    :param template: Для True - необходимо экспортировать данные как шаблон.
    """

    logger.info("Заполнение файла.")
    with open(filename, "w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for date in dates:
            data: List[ThermometryLog] = database.filter(
                return_list=True,
                date=date,
                **({} if group == 0 else {"grp": group}),
            )
            if len(data):
                if template:
                    data.sort(key=lambda x: x.name)
                for obj in data:
                    if template:
                        writer.writerow(
                            ["<TODAY>", "<NONE>", "<NONE>", obj.name, "<NONE>"]
                        )
                    else:
                        writer.writerow(
                            [
                                obj.date,
                                obj.arrival_time,
                                obj.leaving_time,
                                obj.name,
                                obj.temperature,
                            ]
                        )
