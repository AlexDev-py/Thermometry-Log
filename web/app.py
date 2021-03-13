from flask import Flask, render_template, request, jsonify
from database import ThermometryLog
from webview import Window
from datetime import datetime

app = Flask(__name__)
window: Window = ...


@app.route('/')
def home():
    """ Главная """

    date = datetime.now()
    if request.args.get('date'):
        date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')

    return render_template(
        'main.html',
        window=(window.width, window.height),
        date=date.strftime('%Y-%m-%d')
    )


@app.route('/api/getLogs')
def get_logs():
    """
    Получаем записи из базы данных.
    : param date : Дата в формате `%Y-%m-%d` для фильтрации записей.
    """

    date = datetime.now()
    if request.args.get('date'):
        date = datetime.strptime(request.args.get('date'), '%Y-%m-%d')

    ThermometryLogs = ThermometryLog(db_path='database.sqlite')
    logs = ThermometryLogs.filter(
        date=date.strftime('%d.%m.%Y'),
        return_list=True,
        return_type='visual'
    )

    if len(logs):
        average_temp = round(
            sum(map(lambda log: log[2], logs)) / len(logs), 1
        )
        min_temp = min(logs, key=lambda x: x[2])[2]
        max_temp = max(logs, key=lambda x: x[2])[2]
    else:
        average_temp = min_temp = max_temp = 0

    return jsonify(
        logs=logs,
        average_temp=average_temp,
        min_temp=min_temp,
        max_temp=max_temp
    )
