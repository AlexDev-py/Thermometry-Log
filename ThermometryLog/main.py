from datetime import datetime
from typing import NoReturn

import webview
from sqlite3_api import API

import excel
import web.app
from database import ThermometryLog, Float
from logger import logger, LOCAL_APPDATA


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
        logger.info(f'Запись `{log_id}` удалена.')

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
        logger.info(
            f'Запись `{log_id}` изменена.'
            f' новые данные: {name=}, {temperature=}'
        )

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
        logger.info(
            'Добавлена новая запись. '
            f'{name=}, {temperature=}, {date=}'
        )

    @property
    def sql(self):
        """ sqlite3_api.API """

    @sql.getter
    def sql(self) -> API:
        """ Получение нового API """

        return API(DB_PATH)

    @property
    def thermometry_logs(self):
        """ database.ThermometryLog """

    @thermometry_logs.getter
    def thermometry_logs(self) -> ThermometryLog:
        """ Получение нового ThermometryLog """

        return ThermometryLog(DB_PATH)


def open_url(url: str):
    """ Открывает ссылку. """

    logger.info(f'Запрос на переход по адресу `{url}`.')
    window.load_url(f'{REAL_URL}/{url}')


def main() -> NoReturn:
    """ Запуск окна. """

    # Создаём базу данных, если её нет
    ThermometryLog(DB_PATH).create_table()

    def _init(win: webview.Window):
        global REAL_URL
        REAL_URL = win.real_url

    def _on_loaded():
        logger.info(f'Загружена страница `{window.get_current_url()}`')

    def _on_closed():
        logger.info('Окно закрыто.\n')

    def _on_shown():
        logger.info('Окно развернуто.')

    # Добавляем обработчики событий
    window.loaded += _on_loaded
    window.closed += _on_closed
    window.shown += _on_shown

    logger.info('Запуск окна.')
    webview.start(_init, window, debug=True)


logger.info('Создание окна.')
REAL_URL: str = ...  # Ссылка на локальный сервер с приложением
DB_PATH = f'{LOCAL_APPDATA}\database.sqlite'  # Путь к базе данных
web.app.DB_PATH = excel.DB_PATH = DB_PATH

window = webview.create_window(
    'Журнал термометрии', web.app.app, width=1080, height=720,
    easy_drag=False, js_api=JSApi(), min_size=(940, 570)
)
window.expose(open_url)  # Добавляем дополнительные методы к JSApi

if __name__ == '__main__':
    main()
