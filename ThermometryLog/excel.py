"""

Работа с Excel.
Импорт и экспорт данных.

Обрабатываются листы вида:
|   Журнал термометрии на <date>   |
| ФИО           | Температура      |
| <name>        | <temperature>    |
| <name>        | <temperature>    |
| <name>        | <temperature>    |
...

Названием листа должна являться дата.

"""

from datetime import datetime
from typing import List

import openpyxl
from openpyxl.styles import Font, Alignment

from database import ThermometryLog, Float
from logger import logger


def import_data(filename: str, database: ThermometryLog):
    """
    Импортируем данные из книги Excel.
    :param filename: Имя файла.
    :param database: API для работы с базой данных.
    """

    logger.info("Загрузка книги.")
    workbook = openpyxl.load_workbook(filename)  # Открываем книгу

    logger.info("Импорт записей.")
    for sheet_name in workbook.sheetnames:
        try:  # Валидация поля `date`
            date = datetime.strptime(sheet_name, "%d.%m.%Y")
        except ValueError:
            continue

        sheet = workbook[sheet_name]  # Выбираем лист
        rows = sheet.max_row  # Кол-во строк в таблице
        cols = sheet.max_column  # Кол-во колонок в таблице

        if rows <= 2 or cols != 2:
            continue

        for i in range(3, rows + 1):
            # Валидация поля `name`
            if len(name := sheet.cell(i, 1).value) == 0:
                continue
            try:  # Валидация поля `temperature`
                temperature = float(sheet.cell(i, 2).value)
            except ValueError:
                continue

            database.insert(
                name=name,
                temperature=Float(round(temperature, 1)),
                date=date.strftime("%d.%m.%Y"),
            )


def export_data(filename: str, dates: List[str], database: ThermometryLog):
    """
    Экспортируем данные в книгу Excel.
    :param filename: Имя файла.
    :param dates: Даты - названия страниц (в формате '%d.%m.%Y').
    :param database: API для работы с базой данных.
    """

    logger.info("Создание книги.")
    workbook = openpyxl.Workbook()  # Создаем файл
    workbook.remove(workbook["Sheet"])  # Удаляем начальный лист

    logger.info("Заполнение книги.")
    for date in dates:
        data: List[ThermometryLog] = database.filter(return_list=True, date=date)

        if len(data) == 0:
            continue

        sheet = workbook.create_sheet(date)  # Новый лист
        # Размер колонок
        sheet.column_dimensions["A"].width = 18
        sheet.column_dimensions["B"].width = 18
        # Объединяем ячейки A1 и B1
        sheet.merge_cells("A1:B1")
        # Заполняем ячейки
        sheet["A1"] = f"Журнал термометрии на {date}"
        sheet["A1"].font = Font(bold=True)
        sheet["A1"].alignment = Alignment(horizontal="center")
        sheet.append(["ФИО", "Температура"])
        for obj in data:
            sheet.append([obj.name, obj.temperature])

    workbook.save(filename)  # Сохраняем в файл
