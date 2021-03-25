"""

    Сборка приложения в exe.
    Для использования, дополнительно установите cx_Freeze используя
    pip install -U cx_freeze

    Сборка проекта осуществляется в 2 этапа.
    1. Сборка в exe. Осуществляется с помощью cx_Freeze.
    2. Сборка в exe установщик, осуществляемая при помощи nsis.

"""

import cx_Freeze

executables = [
    cx_Freeze.Executable(
        script=r"ThermometryLog\run.py",  # Запускаемый файл
        base="Win32GUI",  # Использует pythonw.exe
        targetName="ThermometryLog.exe",  # Имя exe
        icon="icon.ico",
    )
]
excludes = [
    "unittest",
    "pydoc_data",
    "tkinter",
    "test",
    "pydoc_data",
    "lib2to3",
    "idna",
    "urllib3",
    "asyncio",
    "concurrent",
    "pkg_resources",
]  # Ненужные библиотеки
zip_include_packages = [
    "collections",
    "encodings",
    "importlib",
    "json",
    "click",
    "ctypes",
    "flask",
    "logging",
    "urllib",
    "threading",
    "email",
    "http",
    "html",
    "distutils",
    "multiprocessing",
    "xmlrpc",
    "wsgiref",
    "werkzeug",
    "xml",
    "werkzeug",
    "itsdangerous",
    "sqlite3_api",
    "sqlite3",
    "openpyxl",
    "et_xmlfile",
]  # Библиотеки, помещаемые в архив

cx_Freeze.setup(
    name="Журнал термометрии",
    options={
        "build_exe": {
            "packages": ["webview", "jinja2"],  # Библиотеки
            "include_files": [
                r"ThermometryLog\main.py",
                r"ThermometryLog\web",
                r"ThermometryLog\database.py",
                r"ThermometryLog\logger.py",
                r"ThermometryLog\excel.py",
                r"ThermometryLog\csv_handler.py",
                r"ThermometryLog\tools.py",
            ],  # Файлы проекта
            "excludes": excludes,
            "zip_include_packages": zip_include_packages,
        },
        "build": {"build_exe": "build\ThermometryLog"},  # Место назначения
    },
    version="1.2.0",
    description="Приложение для ведения журнала термометрии.",
    author="AlexDev",
    executables=executables,
)

# python setup.py bdist_msi  # Сборка msi установщика
# python setup.py build  # Сборка exe
