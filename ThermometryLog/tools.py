"""

Инструменты, облегчающие разработку приложения.

"""

import platform
import subprocess
from typing import Union

from webview import Window

from logger import logger

WINDOW: Window = ...  # Окно приложения
js_api = ...  # JSApi из main.py


def loading_modal(div_id: str):
    """
    Загрузочный modal.
    """

    WINDOW.evaluate_js(
        f"""
    document.getElementById('{div_id}').innerHTML = `
    <div class="d-flex justify-content-center py-5">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    `;
    """
    )


def file_modal(div_id: str):
    """
    modal выбора файла.
    """

    WINDOW.evaluate_js(
        f"""
    document.getElementById('{div_id}').innerHTML = `
    <div class="text-center py-5">
        Выберите файл
    </div>
    `;
    """
    )


def submit_form(form_id):
    """
    Закрываем форму и обновляем страницу.
    """

    WINDOW.evaluate_js(f"document.getElementById('{form_id}').submit();")


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
