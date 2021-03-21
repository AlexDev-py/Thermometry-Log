"""

Основной файл.
Может являться пусковым.

Здесь связываются все компоненты приложения.

"""

from datetime import datetime, timedelta
from typing import NoReturn, Literal, Tuple, Union
import json
import subprocess
import platform

import webview
from sqlite3_api import API

import excel
import csv_handler
import web.app
from database import ThermometryLog, Float
from logger import logger, LOCAL_APPDATA


class JSApi:
    """
    Методы, которые будут доступны для использования из JavaScript`а.
    """

    def __init__(self):
        self.real_url: str = ...  # Ссылка на локальный сервер с приложением

    def delete_log(self, log_id: int):
        """
        Удаляем запись под номером `log_id`.
        :param log_id: ID записи, которую нужно удалить.
        """

        sql = self.sql
        sql.execute("DELETE FROM thermometrylog WHERE id=?", log_id)
        sql.commit()
        logger.info("Запись `%s` удалена.", log_id)

    def edit_log(self, log_id: int, name: str, temperature: float):
        """
        Изменяем запись под номером `log_id`.
        :param log_id: ID записи, которую нужно изменить.
        :param name: Новое значение для поля `name`.
        :param temperature: Новое значение для поля `temperature`.
        """

        self.thermometry_logs.filter(id=log_id).update(
            name=name, temperature=Float(temperature)
        )
        logger.info(
            "Запись `%s` изменена." " новые данные: name=%s, temperature=%s",
            log_id,
            name,
            temperature,
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
            date=datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y"),
        )
        logger.info(
            "Добавлена новая запись. " "name=%s, temperature=%s, date=%s",
            name,
            temperature,
            date,
        )

    def import_logs(self):
        """
        Импортируем записи.
        """

        logger.info("Запрос на импортирование данных.")
        file = window.create_file_dialog(
            dialog_type=webview.OPEN_DIALOG,
            file_types=("Excel file (*.xls;*.xlsx;*.xlsm)", "csv file (*.csv)"),
        )  # Получаем путь к нужному файлу

        if file:
            window.evaluate_js(
                """
            document.getElementById('importLogsModalBody').innerHTML = `
            <div class="d-flex justify-content-center">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            `;
            """
            )
            file: str = file[0]
            logger.info("Выбран файл %s", file)
            file_type = file.split(".")[-1]  # Расширение файла

            if file_type in ["xls", "xlsx", "xlsm"]:  # Excel файл
                excel.import_data(file, self.thermometry_logs)
            else:
                csv_handler.import_data(file, self.thermometry_logs)
            logger.info("Импорт завершён.")
        else:
            logger.info("Файл не выбран.")

        window.evaluate_js(
            """
        document.getElementById('importLogsForm').submit();
        """
        )  # Обновляем страницу

    def export_logs(self, file_type: Literal["excel", "csv"], dates: Tuple[str, str]):
        """
        Экспорт записей в excel или csv.
        :param file_type: Куда импортируем.
        :param dates: Временные рамки (в формате '%Y-%m-%d').
        """

        logger.info("Запрос на импортирование файлов.")
        window.evaluate_js(
            """
        document.getElementById('exportLogsModalBody').innerHTML = `
        <div class="text-center py-5">
            Выберите файл
        </div>
        `;
        """
        )

        start_date = datetime.strptime(dates[0], "%Y-%m-%d")
        end_date = datetime.strptime(dates[1], "%Y-%m-%d")
        dates = [
            (start_date + timedelta(days=i)).strftime("%d.%m.%Y")
            for i in range((end_date - start_date).days + 1)
        ]  # Список дат, которые нужно экспортировать

        save_filename = "Журнал термометрии {dates}{ft}".format(
            dates=(dates[0] if dates[0] == dates[-1] else f"{dates[0]} - {dates[-1]}"),
            ft=".xlsx" if file_type == "excel" else ".csv",
        )  # Имя файла для сохранения
        file = window.create_file_dialog(
            dialog_type=webview.SAVE_DIALOG,
            save_filename=save_filename,
        )  # Получаем местоположение файла

        if file:
            window.evaluate_js(
                """
            document.getElementById('exportLogsModalBody').innerHTML = `
            <div class="d-flex justify-content-center py-5">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
            `;
            """
            )
            logger.info("Выбран файл %s", file)

            if file_type == "excel":
                excel.export_data(file, dates, self.thermometry_logs)
            else:
                csv_handler.export_data(file, dates, self.thermometry_logs)
            logger.info("Экспорт завершён.")
        else:
            logger.info("Файл не выбран.")

        window.evaluate_js(
            """
        document.getElementById('exportLogsForm').submit();
        """
        )  # Обновляем страницу

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

    def open_url(self, url: str):
        """ Открывает ссылку. """

        logger.info("Запрос на переход по адресу `%s`.", url)
        window.load_url(f"{self.real_url}/{url}")


def change_color_scheme(color_scheme: Literal["default", "light", "dark"]):
    """
    Изменяем цветовую схему.
    """

    web.app.settings["color_scheme"] = color_scheme
    with open(web.app.SETTINGS_FILE, "w") as settings_file:
        json.dump(web.app.settings, settings_file)

    window.evaluate_js(
        """
    document.getElementById('settingsForm').submit();
    """
    )  # Обновляем страницу


def check_webview2() -> Union["True", "False"]:
    """
    Проверяет наличие WebView2.
    :return: True or False.
    """

    def _cmd(request: str):
        return (
            subprocess.Popen(
                request, text=True, stdout=subprocess.PIPE, encoding="cp866"
            )
            .stdout.read()
            .strip()
        )

    if platform.architecture()[0] == "64bit":
        webview2_status = _cmd(
            "reg flags HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft"
            "\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
        )
    else:
        webview2_status = _cmd(
            "reg flags HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\
            EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
        )

    if webview2_status == "":
        logger.info("WebView2 не найден.")
        return False
    return True


def main() -> NoReturn:
    """ Запуск окна. """

    # Создаём базу данных, если её нет
    ThermometryLog(DB_PATH).create_table()

    def _init(win: webview.Window):
        js_api.real_url = win.real_url

    def _on_loaded():
        logger.info("Загружена страница `%s`", window.get_current_url())

    def _on_closed():
        logger.info("Окно закрыто.\n")

    def _on_shown():
        logger.info("Окно развернуто.")
        if not check_webview2():
            js_api.open_url("/webview2")

    # Добавляем обработчики событий
    window.loaded += _on_loaded
    window.closed += _on_closed
    window.shown += _on_shown

    logger.info("Запуск окна.")
    webview.start(_init, window)


logger.info("Создание окна.")
js_api = JSApi()
DB_PATH = rf"{LOCAL_APPDATA}\database.sqlite"  # Путь к базе данных
web.app.DB_PATH = DB_PATH

window = webview.create_window(
    "Журнал термометрии",
    web.app.app,
    width=1080,
    height=720,
    easy_drag=False,
    js_api=js_api,
    min_size=(940, 570),
)
window.expose(change_color_scheme)  # Добавляем дополнительные методы к JSApi

if __name__ == "__main__":
    main()
