"""

Основной файл.
Может являться пусковым.

Здесь связываются все компоненты приложения.

"""

import json
from datetime import datetime, timedelta
from typing import NoReturn, Literal, Tuple

import webview
from sqlite3_api import API

import csv_handler
import excel
import tools
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

        logger.info("Запрос на удаление записи `%s`.", log_id)
        tools.loading_modal("deleteModalBody")

        sql = self.sql
        sql.execute("DELETE FROM thermometrylog WHERE id=?", log_id)
        sql.commit()

        logger.info("Удалена запись `%s` .", log_id)
        tools.submit_form("deleteForm")

    def edit_log(self, log_id: int, name: str, temperature: float):
        """
        Изменяем запись под номером `log_id`.
        :param log_id: ID записи, которую нужно изменить.
        :param name: Новое значение для поля `name`.
        :param temperature: Новое значение для поля `temperature`.
        """

        logger.info("Запрос на изменение записи `%s`.", log_id)
        tools.loading_modal("editModalBody")

        self.thermometry_logs.filter(id=log_id).update(
            name=name, temperature=Float(temperature)
        )

        logger.info(
            "Изменена запись `%s`. новые данные: name=%s, temperature=%s",
            *(log_id, name, temperature),
        )
        tools.submit_form("editForm")

    def add_log(self, name: str, temperature: float, date: str, group: str):
        """
        Создаем новую запись.
        :param name: ФИО человека.
        :param temperature: Температура.
        :param date: Дата (в формате '%Y-%m-%d').
        :param group: Группа, в которой создаётся запись.
        """

        logger.info("Запрос на создание записи в группе `%s`.", group)
        tools.loading_modal("addModalBody")

        self.thermometry_logs.insert(
            name=name,
            temperature=Float(temperature),
            date=datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y"),
            grp=web.app.groups.get()[group]["id"],
        )

        logger.info(
            "Создана новая запись в группе `%s`. name=%s, temperature=%s, date=%s",
            *(group, name, temperature, date),
        )
        tools.submit_form("addForm")

    def import_logs(self, date: str, group: str):
        """
        Импортируем записи.
        :param date: Дата, на которую импортируются данные (В формате '%Y-%m-%d').
        :param group: Группа, в которую импортируются данные.
        """

        logger.info("Запрос на импортирование данных.")
        group = web.app.groups.get()[group]["id"]
        file = window.create_file_dialog(
            dialog_type=webview.OPEN_DIALOG,
            file_types=(
                "All (*.xls;*.xlsx;*.xlsm;*.csv)",
                "Excel file (*.xls;*.xlsx;*.xlsm)",
                "csv file (*.csv)",
            ),
        )  # Получаем путь к нужному файлу

        if file:
            tools.loading_modal("importLogsModalBody")
            file: str = file[0]
            logger.info("Выбран файл %s", file)
            file_type = file.split(".")[-1]  # Расширение файла

            if file_type in ["xls", "xlsx", "xlsm"]:  # Excel файл
                excel.import_data(file, self.thermometry_logs, group)
            else:
                csv_handler.import_data(file, self.thermometry_logs, date, group)
            logger.info("Импорт завершён.")
        else:
            logger.info("Файл не выбран.")

        tools.submit_form("importLogsForm")

    def export_logs(
        self,
        file_type: Literal["excel", "csv"],
        dates: Tuple[str, str],
        group: str,
        template: bool,
    ):
        """
        Экспорт записей в excel или csv.
        :param file_type: Куда импортируем.
        :param dates: Временные рамки (в формате '%Y-%m-%d').
        :param group: Группа из которой импортируем данные.
        :param template: Для True - необходимо экспортировать данные как шаблон.
        """

        logger.info("Запрос на экспортирование данных.")
        tools.file_modal("exportLogsModalBody")

        group = (web.app.groups.get()[group]["id"], group)
        start_date = datetime.strptime(dates[0], "%Y-%m-%d")
        end_date = datetime.strptime(dates[1], "%Y-%m-%d")
        dates = [
            (start_date + timedelta(days=i)).strftime("%d.%m.%Y")
            for i in range((end_date - start_date).days + 1)
        ]  # Список дат, которые нужно экспортировать

        save_filename = "Журнал термометрии - {group} {dates}{ft}".format(
            group=group[1],
            dates=(dates[0] if dates[0] == dates[-1] else f"{dates[0]} - {dates[-1]}"),
            ft=".xlsx" if file_type == "excel" else (".csvt" if template else ".csv"),
        )  # Имя файла для сохранения
        file = window.create_file_dialog(
            dialog_type=webview.SAVE_DIALOG,
            save_filename=save_filename,
        )  # Получаем местоположение файла

        if file:
            tools.loading_modal("exportLogsModalBody")
            logger.info("Выбран файл %s", file)

            if file_type == "excel":
                excel.export_data(file, dates, self.thermometry_logs, group)
            else:
                csv_handler.export_data(
                    file, dates, self.thermometry_logs, group[0], template
                )
            logger.info("Экспорт завершён.")
        else:
            logger.info("Файл не выбран.")

        tools.submit_form("exportLogsForm")

    def init_group_template(self, group: str, date: str):
        """
        Инициализируем шаблон группы.
        :param group: Группа.
        :param date: Дата, на которую идет инициализация (в формате '%Y-%m-%d').
        """

        group = web.app.groups.get()[group]
        csv_handler.import_data(
            filename=group["template"],
            database=self.thermometry_logs,
            date=date,
            group=group["id"],
        )
        tools.submit_form("waitForm")

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

    logger.info("Запрос на изменение цветовой схемы.")

    web.app.settings["color_scheme"] = color_scheme
    with open(web.app.SETTINGS_FILE, "w") as settings_file:
        json.dump(web.app.settings, settings_file)

    logger.info(f"Цветовая схема изменена на `%s`", color_scheme)
    tools.submit_form("settingsForm")


def add_group(name: str):
    """
    Создаёт новую группу.
    :param name: Название группы.
    """

    logger.info("Запрос на создание группы.")
    tools.loading_modal("addModalBody")

    groups = web.app.groups.get()
    if name in groups:
        window.evaluate_js("alert('Группа с таким названием уже существует.')")
    else:
        tools.file_modal("addModalBody")
        file = window.create_file_dialog(
            dialog_type=webview.OPEN_DIALOG,
            file_types=("csv template file (*.csvt)",),
        )  # Получаем путь к шаблону

        tools.loading_modal("addModalBody")

        if file:
            file = file[0]
            logger.info("Выбран шаблон %s", file)
        else:
            file = None
            logger.info("Шаблон не выбран.")

        web.app.groups.add_group(name, file)
        logger.info("Создана группа. name=%s, template=%s", name, file)

    tools.submit_form("addForm")


def delete_group(name: str):
    """
    Удаляет группу.
    :param name: Имя группы.
    """

    logger.info("Запрос на удаление группы `%s`.", name)
    tools.loading_modal("deleteModalBody")

    _id = web.app.groups.del_group(name)
    sql = js_api.sql
    sql.execute("DELETE FROM thermometrylog WHERE grp=?", _id)
    sql.commit()
    logger.info("Удалена группа `%s`", name)

    tools.submit_form("deleteForm")


def edit_group(old_name: str, new_name: str):
    """
    Изменяем группу.
    :param old_name: Старое название группы.
    :param new_name: Новое название группы.
    """

    logger.info("Запрос на изменение группы `%s`.", old_name)

    tools.file_modal("editModalBody")
    file = window.create_file_dialog(
        dialog_type=webview.OPEN_DIALOG,
        file_types=("csv template file (*.csvt)",),
    )  # Получаем путь к шаблону

    tools.loading_modal("editModalBody")

    if file:
        file = file[0]
        logger.info("Выбран шаблон %s", file)
    else:
        file = None
        logger.info("Шаблон не выбран.")

    web.app.groups.edit_group(old_name, new_name, file)
    logger.info(
        "Изменена группа `%s`. новые данные: name=%s, template=%s",
        *(old_name, new_name, file),
    )

    tools.submit_form("editForm")


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
        if not tools.check_webview2():
            js_api.open_url("/webview2")

    # Добавляем обработчики событий
    window.loaded += _on_loaded
    window.closed += _on_closed
    window.shown += _on_shown

    logger.info("Запуск окна.")
    webview.start(_init, window, debug=True)


logger.info("Создание окна.")
js_api = tools.js_api = JSApi()
DB_PATH = rf"{LOCAL_APPDATA}\database.sqlite"  # Путь к базе данных
web.app.DB_PATH = DB_PATH

window = web.app.WINDOW = tools.WINDOW = webview.create_window(
    "Журнал термометрии",
    web.app.app,
    width=1080,
    height=720,
    easy_drag=False,
    js_api=js_api,
    min_size=(940, 570),
)
# Добавляем дополнительные методы к JSApi
window.expose(change_color_scheme, add_group, delete_group, edit_group)

if __name__ == "__main__":
    main()
