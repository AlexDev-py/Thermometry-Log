"""

Веб-приложение.

"""

import difflib
import os
import re
import json
from datetime import datetime
from typing import List

from flask import Flask, render_template, request

from database import ThermometryLog, Float
from logger import logger, LOCAL_APPDATA

logger.info("Создание веб-приложения.")
DB_PATH: str = ...  # Путь к базе данных

# Настройка окружения. (При сборке приложения)
ROOT = os.path.abspath(__file__)
if ROOT.endswith(".pyc"):
    ROOT = "/".join(ROOT.split("\\")[:-4])
else:
    ROOT = "/".join(ROOT.split("\\")[:-2])

app = Flask(
    __name__,
    template_folder=f"{ROOT}/web/templates",
    static_folder=f"{ROOT}/web/static",
)

SETTINGS_FILE = rf"{LOCAL_APPDATA}\settings.json"
if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as settings_file:
        settings = {"color_scheme": "default"}
        json.dump(settings, settings_file)
else:
    with open(SETTINGS_FILE) as settings_file:
        settings = json.load(settings_file)
del settings_file


@app.route("/")
def home():
    """ Главная """

    logger.info("Запрос на главную страницу с параметрами %s.", dict(request.args))

    date = datetime.now()
    if request.args.get("date"):
        date = datetime.strptime(request.args.get("date"), "%Y-%m-%d")

    logger.info("Получение записей.")
    logs: List[ThermometryLog] = ThermometryLog(DB_PATH).filter(
        date=date.strftime("%d.%m.%Y"),
        return_list=True,
    )

    if len(logs):
        average_temp = round(sum(map(lambda log: log.temperature, logs)) / len(logs), 1)
        min_temp = min(logs, key=lambda x: x.temperature).temperature
        max_temp = max(logs, key=lambda x: x.temperature).temperature
    else:
        average_temp = min_temp = max_temp = 0

    logger.info("Отправка ответа.")
    return render_template(
        "main.html",
        color_scheme=settings["color_scheme"],
        logs=logs[::-1],
        average_temp=average_temp,
        min_temp=min_temp,
        max_temp=max_temp,
        date=date.strftime("%Y-%m-%d"),
        now_date=datetime.now().strftime("%Y-%m-%d"),
    )


@app.route("/search")
def search():
    """
    Производит поиск.
    : param date : Дата, для поиска.
    : param search : Поисковый запрос.
        Может принимать температуру или ФИО человека.
    """

    logger.info("Запрос на страницу поиска с параметрами %s.", dict(request.args))

    condition: str = request.args.get("search").lower()  # Поисковый запрос
    date = datetime.strptime(request.args.get("date"), "%Y-%m-%d")
    thermometry_log = ThermometryLog(DB_PATH)

    # Если передана температура
    if re.fullmatch(r"\d+[.,]\d+", condition) or condition.isdigit():
        logger.info("Получение записей.")
        condition: float = Float(round(float(condition.replace(",", ".")), 1))
        results = thermometry_log.filter(temperature=condition, return_list=True)
        results.sort(key=lambda log: log.date, reverse=True)
        logger.info("Отправка ответа.")
        return render_template(
            "search_temp.html",
            data=results,
            date=date.strftime("%Y-%m-%d"),
            condition=condition,
        )

    logger.info("Получение записей.")
    logs = thermometry_log.filter(return_list=True)
    names = set(log.name for log in logs)  # Всё ФИО
    # Ищем наиболее похожие
    fuzz = difflib.get_close_matches(condition, names)

    result = dict(
        fullmatch=[
            log for log in logs if log.name.lower() == condition
        ],  # Результаты с полным совпадением по запросу
        other=[
            log for log in logs if log.name in fuzz and log.name.lower() != condition
        ],  # Похожие результаты
    )

    if len(result["fullmatch"]):
        average_temp = round(
            sum(map(lambda log: log.temperature, result["fullmatch"]))
            / len(result["fullmatch"]),
            1,
        )
        min_temp = min(result["fullmatch"], key=lambda x: x.temperature).temperature
        max_temp = max(result["fullmatch"], key=lambda x: x.temperature).temperature
    else:
        average_temp = min_temp = max_temp = 0

    logger.info("Отправка ответа.")
    return render_template(
        "search_name.html",
        color_scheme=settings["color_scheme"],
        data=result,
        date=date.strftime("%Y-%m-%d"),
        condition=condition,
        average_temp=average_temp,
        min_temp=min_temp,
        max_temp=max_temp,
    )
