"""

    Сборка exe и msi

"""

import cx_Freeze

executables = [
    cx_Freeze.Executable(
        script=r'ThermometryLog\run.py',
        # base='Win32GUI',
        targetName='ThermometryLog.exe',
        icon='icon.ico'
    )
]
excludes = [
    'unittest', 'pydoc_data', 'xml',
    'test', 'idna', 'urllib3', 'asyncio', 'concurrent'
]
zip_include_packages = [
    'collections', 'encodings', 'importlib', 'json', 'click', 'ctypes', 'flask',
    'logging', 'urllib', 'threading', 'email', 'http', 'html', 'distutils',
    'jinja2', 'multiprocessing', 'xmlrpc', 'wsgiref', 'werkzeug',
    'werkzeug', 'itsdangerous', 'sqlite3_api', 'sqlite3'
]

cx_Freeze.setup(
    name='Журнал термометрии',
    options={
        'build_exe': {
            'packages': [
                'webview', 'flask', 'jinja2', 'logging', 'sqlite3_api'
            ],
            'include_files': [
                r'ThermometryLog\main.py', r'ThermometryLog\web',
                r'ThermometryLog\database.py', r'ThermometryLog\logger.py',
            ],
            'excludes': excludes,
            'zip_include_packages': zip_include_packages},
        'build': {
            'build_exe': 'build\ThermometryLog'
        }
    },

    version='1.0.0',
    description='Приложение для ведения журнала термометрии.',
    author='AlexDev',

    executables=executables,
)

# python setup.py bdist_msi
# python setup.py build
