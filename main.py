import webview
import web.app
from sqlite3_api import API
from database import ThermometryLog, Float
from datetime import datetime
import json


class JSApi:
    """
    Методы, которые будут доступны для использования из JavaScript`а.
    """

    def delete_log(self, log_id: int):
        """
        Удаляем запись под номером `log_id`.
        :param log_id: ID записи, которую нужно удалить.
        """

        sql = self.sql
        sql.execute(f'DELETE FROM thermometrylog WHERE id=?', log_id)
        sql.commit()

    def edit_log(self, log_id: int, name: str, temperature: float):
        """
        Изменяем запись под номером `log_id`.
        :param log_id: ID записи, которую нужно изменить.
        :param name: Новое значение для поля `name`.
        :param temperature: Новое значение для поля `temperature`.
        """

        self.thermometry_logs.filter(id=log_id).update(
            name=name,
            temperature=Float(temperature)
        )

    def get_logs(self, date: str = None) -> json.dumps:
        """
        Получаем записи из базы данных.
        :param date: Дата в формате `%Y-%m-%d` для фильтрации записей.
        """

        if date:
            date = datetime.strptime(date, '%Y-%m-%d')
        else:
            date = datetime.now()

        logs = self.thermometry_logs.filter(
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

        return json.dumps(dict(
            logs=logs,
            average_temp=average_temp,
            min_temp=min_temp,
            max_temp=max_temp
        ))

    def add_log(self, name: str, temperature: float, date: str):
        """
        Создаем новую запись.
        :param name: ФИО человека.
        :param temperature: Температура.
        :param date: Дата в формате `%Y-%m-%d`.
        """

        self.thermometry_logs.insert(
            name=name,
            temperature=Float(temperature),
            date=datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')
        )

    @property
    def sql(self):
        """ sqlite3_api.API """

    @sql.getter
    def sql(self) -> API:
        """ Получение нового API """

        return API(db_path='database.sqlite')

    @property
    def thermometry_logs(self):
        """ database.ThermometryLog """

    @thermometry_logs.getter
    def thermometry_logs(self) -> ThermometryLog:
        """ Получение нового ThermometryLog """

        return ThermometryLog(db_path='database.sqlite')


def open_url(url: str):
    """ Открывает ссылку """

    window.load_url(f'{REAL_URL}/{url}')


def destroy_app():
    """ Закрывает приложение """

    window.destroy()


def hide_app():
    """ Сворачивает/разворачивает окно """

    window.minimize()


def loaded():
    """ Вызывается после загрузки DOM. """

    window.evaluate_js('get_logs()')


def _init(win):
    global REAL_URL
    REAL_URL = win.real_url


REAL_URL: str = ...  # Ссылка на локальный сервер с приложением
web.app.window = window = webview.create_window(
    'Журнал термометрии', web.app.app, width=1080, height=720,
    frameless=True, easy_drag=False, js_api=JSApi()
)
window.loaded += loaded
window.expose(open_url, destroy_app, hide_app)
webview.start(_init, window, debug=True, gui='gt')
