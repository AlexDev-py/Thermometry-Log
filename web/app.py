from flask import Flask, render_template, request
from webview import Window
from datetime import datetime
from database import ThermometryLog
from typing import List

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
        logs=logs,
        average_temp=average_temp,
        min_temp=min_temp,
        max_temp=max_temp,
        window=(window.width, window.height),
        date=date.strftime('%Y-%m-%d'),
        now_date=datetime.now().strftime('%Y-%m-%d')
    )
