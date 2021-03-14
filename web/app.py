from flask import Flask, render_template, request
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
