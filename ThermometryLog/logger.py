"""

Настройка логирования.

"""

import logging.config
import os

LOCAL_APPDATA = (
        '/'.join(os.getenv('APPDATA').split('\\')[:-1]) +
        '/Local/ThermometryLog'
)  # ...\AppData\Local\ThermometryLog
LOG_FILE = LOCAL_APPDATA + '/logs.log'  # Путь к файлу для записи логов

# Создаём директорию, если её нет
if not os.path.exists(LOCAL_APPDATA):
    os.mkdir(LOCAL_APPDATA)

# Конфигурация логера
dictLogConfig = {
    'version': 1,
    'handlers': {
        'fileHandler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'myFormatter',
            'filename': LOG_FILE
        },
        'consoleHandler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'myFormatter'
        }
    },
    'loggers': {
        '': {
            'handlers': ['fileHandler', 'consoleHandler'],
            'level': 'INFO',
        }
    },
    'formatters': {
        'myFormatter': {
            'format': '%(asctime)s - [%(levelname)s] - '
                      '(%(filename)s).%(funcName)s - %(message)s'
        }
    }
}

logging.config.dictConfig(dictLogConfig)
logger = logging.getLogger()
