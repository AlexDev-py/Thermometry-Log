"""

Работа с Excel.
Импорт и экспорт данных.

Обрабатываются таблицы вида:
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

DB_PATH: str = ...  # Путь к базе данных


def import_data(filename: str):
    """
    Импортируем данные из файла Excel.
    :param filename: Имя файла.
    """

    thermometry_log = ThermometryLog(DB_PATH)
    workbook = openpyxl.load_workbook(filename)  # Открываем файл

    for sheet_name in workbook.sheetnames:
        try:
            date = datetime.strptime(sheet_name, '%d.%m.%Y')
        except ValueError:
            continue

        sheet = workbook[sheet_name]  # Выбираем лист
        rows = sheet.max_row  # Кол-во строк в таблице
        cols = sheet.max_column  # Кол-во колонок в таблице

        if rows <= 2 or cols != 2:
            continue

        for i in range(3, rows + 1):
            if len(name := sheet.cell(i, 1).value) == 0:
                continue
            try:
                temperature = float(sheet.cell(i, 2).value)
            except ValueError:
                continue

            thermometry_log.insert(
                name=name,
                temperature=Float(round(temperature, 1)),
                date=date.strftime('%d.%m.%Y')
            )


def export_data(filename: str, dates: List[str]):
    """
    Экспортируем данные в файл Excel.
    :param filename: Имя файла.
    :param dates: Даты - названия страниц (в формате '%d.%m.%Y').
    """

    thermometry_log = ThermometryLog(DB_PATH)
    workbook = openpyxl.Workbook()  # Создаем файл
    workbook.remove(workbook['Sheet'])  # Удаляем начальный лист

    for date in dates:
        data: List[ThermometryLog] = thermometry_log.filter(
            return_list=True, date=date
        )

        if not len(data):
            continue

        sheet = workbook.create_sheet(date)  # Новый лист
        # Размер колонок
        sheet.column_dimensions['A'].width = 18
        sheet.column_dimensions['B'].width = 18
        # Объединяем ячейки A1 и B1
        sheet.merge_cells('A1:B1')
        # Заполняем ячейки
        sheet['A1'] = f'Журнал термометрии на {date}'
        sheet['A1'].font = Font(bold=True)
        sheet['A1'].alignment = Alignment(horizontal='center')
        sheet.append(['ФИО', 'Температура'])
        for obj in data:
            sheet.append([obj.name, obj.temperature])

    workbook.save(filename)  # Сохраняем в файл
