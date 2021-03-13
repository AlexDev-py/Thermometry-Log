import webview
import web.app
from sqlite3_api import API
from database import ThermometryLog, Float


REAL_URL: str = ...  # Ссылка на локальный сервер с приложением


def main():
    window = webview.create_window(
        'Журнал термометрии', web.app.app, width=1080, height=720,
        frameless=True, easy_drag=False
    )
    web.app.window = window

    def open_url(url: str):
        """ Открывает ссылку """
        print(f'{REAL_URL}/{url}')
        window.load_url(f'{REAL_URL}/{url}')

    def destroy_app():
        """ Закрывает приложение """
        window.destroy()

    def hide_app():
        """ Сворачивает/разворачивает окно """
        window.minimize()

    def delete_log(log_id: int):
        """ Удаляем запись под номером `log_id` """
        sql = API(db_path='database.sqlite')
        sql.execute(f'DELETE FROM thermometrylog WHERE id=?', log_id)
        sql.commit()

    def edit_log(log_id: int, name: str, temp: float):
        """ Изменяем запись под номером `log_id` """
        ThermometryLog('database.sqlite').filter(id=log_id).update(
            name=name,
            temperature=Float(temp)
        )

    window.expose(
        destroy_app, hide_app, open_url, delete_log, edit_log
    )

    def _init(win):
        global REAL_URL
        REAL_URL = win.real_url
        print(REAL_URL)

    webview.start(_init, window, debug=True, gui='gt')


if __name__ == '__main__':
    main()
