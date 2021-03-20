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
        return Float(obj.decode("utf-8"))


class ThermometryLog(Table):
    """
    Класс описывающий структуру хранения данных в таблице.
    """

    name: str  # ФИО человека, у которого измеряли температуру
    temperature: Float  # Температура человека
    date: str  # Дата измерения в формате `%d.%m.%Y` (<день>.<месяц>.<год>)
