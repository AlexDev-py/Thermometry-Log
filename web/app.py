from flask import Flask, render_template, request
from webview import Window
from datetime import datetime
from database import ThermometryLog, Float
from typing import List
import re
import difflib

app = Flask(__name__)
window: Window = ...


@app.route('/')
def home():
    """ Главная """

    date = datetime.now()
    if request.args.get('date'):
        date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')

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

    condition: str = request.args.get('search').lower()
    date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')
    thermometry_log = ThermometryLog(db_path='database.sqlite')

    # Если передана температура
    if re.fullmatch(r'\d+[.,]\d+', condition) or condition.isdigit():
        condition: float = Float(round(float(condition.replace(',', '.')), 1))
        results = thermometry_log.filter(
            temperature=condition,
            return_list=True
        )
        results.sort(key=lambda log: log.date, reverse=True)
        return render_template(
            'search_temp.html',
            window=(window.width, window.height),
            data=results,
            date=date.strftime('%Y-%m-%d'),
            condition=condition
        )
    else:
        logs = thermometry_log.filter(return_list=True)
        names = list(log.name for log in logs)
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
