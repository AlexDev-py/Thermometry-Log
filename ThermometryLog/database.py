"""

Таблицы, хранящиеся в базе данных.

"""

from __future__ import annotations
from typing import Union

import json
import os

from sqlite3_api import Table
from sqlite3_api.field_types import CustomType

from logger import LOCAL_APPDATA

GROUPS_FILE = rf"{LOCAL_APPDATA}\groups.json"


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
    grp: int = 0  # Группа, к которой относится человек (default: общая)
    arrival_time: str  # Время измерения в формате `<час>:<минута>`
    leaving_time: str = "0"  # Время ухода в формате `<час>:<минута>`


class Groups:
    """
    Группы пользователей.
    """

    def __init__(self):
        if not os.path.exists(GROUPS_FILE):
            with open(GROUPS_FILE, "w", encoding="utf-8") as file:
                json.dump({"Общая": {"template": None, "id": 0}}, file)

    @staticmethod
    def get() -> dict:
        """
        Возвращает группы.
        :return: {"<Название группы>": {"template": <путь к шаблону>/None}}
        """

        with open(GROUPS_FILE, encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def save(data: dict):
        """
        Сохраняет группы.
        :param data: Данные, полученные методом `Groups.get()`
        """

        with open(GROUPS_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file)

    @staticmethod
    def add_group(name: str, template: Union[str, None], _id: int = None) -> int:
        """
        Создает новую группу.
        :param name: Название группы.
        :param template: Путь к шаблону.
        :param _id: ID новой группы (Создаётся автоматически).
        :return: ID новой группы.
        """

        groups = Groups.get()
        _id = _id or max([x["id"] for x in groups.values()]) + 1
        groups[name] = {"template": template, "id": _id}
        Groups.save(groups)
        return _id

    @staticmethod
    def del_group(name: str) -> int:
        """
        Удаляет группу.
        :param name: Название группы.
        :return: ID группы.
        """

        groups = Groups.get()
        _id = groups[name]
        del groups[name]
        Groups.save(groups)
        return _id["id"]

    @staticmethod
    def edit_group(old_name: str, new_name: str, template: Union[str, None]) -> int:
        """
        Редактирует группу.
        :param old_name: Старое название группы.
        :param new_name: Новое название группы.
        :param template: Путь к шаблону.
        :return: ID группы.
        """

        return Groups.add_group(
            name=new_name, template=template, _id=Groups.del_group(old_name)
        )
