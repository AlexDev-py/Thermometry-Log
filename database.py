"""

Таблицы, хранящиеся в базе данных.

"""

from __future__ import annotations

from sqlite3_api import Table
from sqlite3_api.field_types import CustomType


class Float(CustomType, float):
    """
    Тип данных, для хранения чисел с плавающей точкой.
    """

    def converter(self, obj: bytes) -> Float:
        return Float(obj.decode('utf-8'))


class ThermometryLog(Table):
    """
    Класс описывающий структуру хранения данных в таблице.
    """

    name: str  # ФИО человека, у которого измеряли температуру
    temperature: Float  # Температура человека
    date: str  # Дата измерения в формате `%d.%m.%Y` (<день>.<месяц>.<год>)


if __name__ == '__main__':
    import random
    ThermometryLogs = ThermometryLog(db_path='database.sqlite')
    ThermometryLogs.create_table()
    names = [
        'AlexDev', 'Konan', 'Naruto', 'James Arthur Gosling',
        'Bjarne Stroustrup', 'Guido van Rossum'
    ]
    for d in range(10, 15):
        for _ in range(20):
            ThermometryLogs.insert(
                name=random.choice(names),
                temperature=Float(round(random.uniform(35.0, 38.0), 1)),
                date=f'{d}.03.2021'
            )
    # ThermometryLogs.insert(name='James Arthur Gosling Java', temperature=36.3, date='12.03.2021')
    # ThermometryLogs.insert(name='Bjarne Stroustrup', temperature=36.5, date='12.03.2021')
