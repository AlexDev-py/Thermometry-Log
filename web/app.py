"""

Веб-приложение.

"""

import difflib
import logging.config
import re
from datetime import datetime
from typing import List

from flask import Flask, render_template, request
from webview import Window

from database import ThermometryLog, Float

logging.config.fileConfig('logging.cfg')
logger = logging.getLogger()
logger.info('Создание веб-приложения.')
app = Flask(__name__)
window: Window = ...


@app.route('/')
def home():
    """ Главная """

    logger.info(
        'Запрос на главную страницу '
        f'с параметрами {dict(request.args)}.'
    )
    date = datetime.now()
    if request.args.get('date'):
        date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')

    logger.info('Получение записей.')
    logs: List[ThermometryLog] = ThermometryLog('database.sqlite').filter(
        date=date.strftime('%d.%m.%Y'),
        return_list=True,
    )

    if len(logs):
        average_temp = round(
            sum(map(lambda log: log.temperature, logs)) / len(logs), 1
        )
        min_temp = min(logs, key=lambda x: x.temperature).temperature
        max_temp = max(logs, key=lambda x: x.temperature).temperature
    else:
        average_temp = min_temp = max_temp = 0

    logger.info('Отправка ответа.')
    return render_template(
        'main.html',
        logs=logs[::-1],
        average_temp=average_temp,
        min_temp=min_temp,
        max_temp=max_temp,
        window=(window.width, window.height),
        date=date.strftime('%Y-%m-%d'),
        now_date=datetime.now().strftime('%Y-%m-%d')
    )


@app.route('/search')
def search():
    """
    Производит поиск.
    : param date : Дата, для поиска.
    : param search : Поисковый запрос.
        Может принимать температуру или ФИО человека.
    """

    logger.info(
        'Запрос на страницу поиска '
        f'с параметрами {dict(request.args)}.'
    )
    condition: str = request.args.get('search').lower()
    date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
    thermometry_log = ThermometryLog(db_path='database.sqlite')

    # Если передана температура
    if re.fullmatch(r'\d+[.,]\d+', condition) or condition.isdigit():
        logger.info('Получение записей.')
        condition: float = Float(round(float(condition.replace(',', '.')), 1))
        results = thermometry_log.filter(
            temperature=condition,
            return_list=True
        )
        results.sort(key=lambda log: log.date, reverse=True)
        logger.info('Отправка ответа.')
        return render_template(
            'search_temp.html',
            window=(window.width, window.height),
            data=results,
            date=date.strftime('%Y-%m-%d'),
            condition=condition
        )
    else:
        logger.info('Получение записей.')
        logs = thermometry_log.filter(return_list=True)
        names = set(log.name for log in logs)
        fuzz = difflib.get_close_matches(condition, names)
        result = dict(
            fullmatch=[
                log for log in logs
                if log.name.lower() == condition
            ],
            other=[
                log for log in logs
                if log.name in fuzz and log.name.lower() != condition
            ]
        )
        if len(result['fullmatch']):
            average_temp = round(sum(map(
                lambda log: log.temperature, result['fullmatch'])
            ) / len(result['fullmatch']), 1)
            min_temp = min(
                result['fullmatch'], key=lambda x: x.temperature
            ).temperature
            max_temp = max(
                result['fullmatch'], key=lambda x: x.temperature
            ).temperature
        else:
            average_temp = min_temp = max_temp = 0
        logger.info('Отправка ответа.')
        return render_template(
            'search_name.html',
            window=(window.width, window.height),
            data=result,
            date=date.strftime('%Y-%m-%d'),
            condition=condition,
            average_temp=average_temp,
            min_temp=min_temp,
            max_temp=max_temp,
        )
