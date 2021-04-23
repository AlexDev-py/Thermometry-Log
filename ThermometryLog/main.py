"""

Основной файл.
Может являться пусковым.

Здесь связываются все компоненты приложения.

"""

import csv
import json
from datetime import datetime, timedelta
from typing import NoReturn, Literal, Tuple, List

import webview

import csv_handler
import excel
import tools
import web.app
from database import ThermometryLog, Float
from logger import logger, LOCAL_APPDATA
from sqlite3_api import API


class JSApi:
    """
    Методы, которые будут доступны для использования из JavaScript`а.
    """

    def __init__(self):
        self.real_url: str = ...  # Ссылка на локальный сервер с приложением

    def delete_log(self, log_id: int):
        """
        Удаляет запись под номером `log_id`.
        :param log_id: ID записи, которую нужно удалить.
        """

        logger.info("Запрос на удаление записи `%s`.", log_id)
        tools.loading_modal("deleteModalBody")

        sql = self.sql
        # Не заменять на self.sql.execute()!
        sql.execute("DELETE FROM thermometrylog WHERE id=?", log_id)
        sql.commit()

        logger.info("Удалена запись `%s` .", log_id)
        tools.submit_form("deleteForm")

    def edit_log(self, log_id: int, name: str, temperature: float):
        """
        Изменяет запись под номером `log_id`.
        :param log_id: ID записи, которую нужно изменить.
        :param name: Новое значение для поля `name`.
        :param temperature: Новое значение для поля `temperature`.
        """

        logger.info("Запрос на изменение записи `%s`.", log_id)
        tools.loading_modal("editModalBody")

        log = self.thermometry_logs.filter(id=log_id)
        log.update(
            name=name,
            temperature=Float(temperature),
            time=log.time if log.time != "0" else datetime.now().strftime("%H:%M"),
        )

        logger.info(
            "Изменена запись `%s`. новые данные: name=%s, temperature=%s",
            *(log_id, name, temperature),
        )
        tools.submit_form("editForm")

    def add_log(self, name: str, temperature: float, date: str, group: str):
        """
        Создает новую запись.
        :param name: ФИО человека.
        :param temperature: Температура.
        :param date: Дата (в формате '%Y-%m-%d').
        :param group: Группа, в которой создаётся запись.
        """

        logger.info("Запрос на создание записи в группе `%s`.", group)
        tools.loading_modal("addModalBody")
        time = datetime.now().strftime("%H:%M")  # Текущее время

        self.thermometry_logs.insert(
            name=name,
            temperature=Float(temperature),
            date=datetime.strptime(date, "%Y-%m-%d").strftime("%d.%m.%Y"),
            grp=web.app.groups.get()[group]["id"],
            time=time,
        )

        logger.info(
            "Создана новая запись в группе `%s`. name=%s, temperature=%s, date=%s, time=%s",
            *(group, name, temperature, date, time),
        )
        tools.submit_form("addForm")

    def global_edit(self, name: str, temperature: float, date: str, group: str):
        """
        Редактирует или добавляет запись в группе.
        :param name: ФИО человека.
        :param temperature: Температура.
        :param date: Дата (в формате '%Y-%m-%d').
        :param group: Группа, в которой редактируется/создаётся запись.
        """

        logger.info("Запрос на изменение записи в группе %s. name=`%s`.", group, name)
        tools.loading_modal("globalEditModalBody")
        date = datetime.strptime(date, "%Y-%m-%d")
        group = web.app.groups.get()[group]  # Нужная группа
        log: List[ThermometryLog] = self.thermometry_logs.filter(
            date=date.strftime("%d.%m.%Y"),
            grp=group["id"],
            name=name,
            return_list=True,
        )

        if len(log) == 1:
            log: ThermometryLog = log[0]  # Нужная запись
            if log.time == "0":  # Если нет данных
                log.update(
                    temperature=Float(temperature),
                    time=datetime.now().strftime("%H:%M"),
                )
                logger.info(
                    "Изменена запись в группе %s. данные: name=%s, temperature=%s",
                    *(group["id"], name, temperature),
                )
                return tools.submit_form("globalEditForm")

        self.thermometry_logs.insert(
            name=name,
            temperature=Float(temperature),
            date=date.strftime("%d.%m.%Y"),
            grp=group["id"],
            time=datetime.now().strftime("%H:%M"),
        )
        logger.info(
            "Создана новая запись в группе `%s`. name=%s, temperature=%s, date=%s",
            *(group, name, temperature, date),
        )

        tools.submit_form("globalEditForm")

    def import_logs(self, date: str, group: str):
        """
        Импортирует записи.
        :param date: Дата, на которую импортируются данные (В формате '%Y-%m-%d').
        :param group: Группа, в которую импортируются данные.
        """

        logger.info("Запрос на импортирование данных.")
        group = web.app.groups.get()[group]["id"]
        file = window.create_file_dialog(
            dialog_type=webview.OPEN_DIALOG,
            file_types=(
                "All (*.xls;*.xlsx;*.xlsm;*.csv;*.csvt)",
                "Excel file (*.xls;*.xlsx;*.xlsm)",
                "csv file (*.csv)",
                "csv template file (*.csvt)",
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
        Экспортирует записи в excel или csv.
        :param file_type: Куда импортирует.
        :param dates: Временные рамки (в формате '%Y-%m-%d').
        :param group: Группа из которой импортирует данные.
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

    def init_groups(self, groups: str):
        """
        Инициализирует шаблоны групп.
        :param groups: Названия групп через ';'.
        """

        all_groups = web.app.groups.get()  # Все группы
        if len(groups):
            for group in groups.split(";"):
                group = all_groups[group]
                csv_handler.import_data(
                    filename=group["template"],
                    database=self.thermometry_logs,
                    date=datetime.now().strftime("%Y-%m-%d"),
                    group=group["id"],
                )

    @property
    def sql(self):
        """ sqlite3_api.API """

    @sql.getter
    def sql(self) -> API:
        """ Получение нового API """

        return API(DB_PATH)  # Необходимо, так как sqlite3 не работает в разных потоках

    @property
    def thermometry_logs(self):
        """ database.ThermometryLog """

    @thermometry_logs.getter
    def thermometry_logs(self) -> ThermometryLog:
        """ Получение нового ThermometryLog """

        return ThermometryLog(
            DB_PATH
        )  # Необходимо, так как sqlite3 не работает в разных потоках

    def open_url(self, url: str):
        """ Открывает ссылку. """

        logger.info("Запрос на переход по адресу `%s`.", url)
        window.load_url(f"{self.real_url}/{url}")


def change_color_scheme(color_scheme: Literal["default", "light", "dark"]):
    """
    Изменяет цветовую схему.
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

        group_id = web.app.groups.add_group(name, file)
        if file:
            csv_handler.import_data(
                filename=file,
                database=js_api.thermometry_logs,
                date=datetime.now().strftime("%Y-%m-%d"),
                group=group_id,
            )  # Инициализируем шаблон
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
    sql.execute(
        "DELETE FROM thermometrylog WHERE grp=?", _id
    )  # Удаляем все записи группы
    sql.commit()
    logger.info("Удалена группа `%s`", name)

    tools.submit_form("deleteForm")


def edit_group(old_name: str, new_name: str):
    """
    Изменяет группу.
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


def get_group_members(name: str) -> list:
    """
    Возвращает участников группы.
    :param name: Название группы.
    :return: Список имён.
    """

    names = []
    if len(name) == 0:
        return names

    group = web.app.groups.get()[name]
    if group["template"]:
        with open(group["template"], encoding="utf-8-sig") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(name := row[2]) != 0:
                    if name not in names:
                        names.append(name)

    return names


def main() -> NoReturn:
    """ Запуск окна. """

    # Создаём базу данных, если её нет
    ThermometryLog(DB_PATH).create_table()

    def _init(win: webview.Window):
        js_api.real_url = win.real_url
        win.load_url(f"{win.real_url}/start")

    def _on_loaded():
        logger.info("Загружена страница `%s`", window.get_current_url())

    def _on_closed():
        logger.info("Окно закрыто.\n")

    def _on_shown():
        logger.info("Окно развернуто.")
        if not tools.check_webview2():
            js_api.open_url("/webview2")

    def _run():
        globals()["window"] = web.app.WINDOW = tools.WINDOW = webview.create_window(
            "Журнал термометрии",
            web.app.app,
            width=1080,
            height=720,
            easy_drag=False,
            js_api=js_api,
            min_size=(940, 570),
        )

        # Добавляем дополнительные методы к JSApi
        window.expose(
            change_color_scheme, add_group, delete_group, edit_group, get_group_members
        )

        # Добавляем обработчики событий
        window.loaded += _on_loaded
        window.closed += _on_closed
        window.shown += _on_shown

        start_window.destroy()  # Закрываем стартовое окно

    start_window = webview.create_window(
        "Журнал термометрии",
        web.app.app,
        width=150,
        height=200,
        easy_drag=True,
        frameless=True,
        resizable=False,
        js_api=js_api,
        min_size=(100, 100),
    )  # Стартовое окно
    start_window.expose(_run)  # Добавляем методы к JSApi

    logger.info("Запуск окна.")
    webview.start(_init, start_window, debug=True)


logger.info("Создание окна.")
js_api = tools.js_api = JSApi()
DB_PATH = rf"{LOCAL_APPDATA}\database.sqlite"  # Путь к базе данных
web.app.DB_PATH = DB_PATH

window = web.app.WINDOW = tools.WINDOW = ...

if __name__ == "__main__":
    main()
