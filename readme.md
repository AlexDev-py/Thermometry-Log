# Журнал термометрии [![](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

В связи с ситуацией с COVID-19 во многим учреждениям были введены
обязательные журналы термометрии на бумажных носителях.
Не исключением стали также образовательные организации. 
Ключевой проблемой стало неудобство занесение и
хранение данных об обучающихся, а также о сотрудниках.

Данное приложение решает эти проблемы! 
- У приложения понятный интерфейс, так что любой 
с лёгкостью может работать в нём.
- Ваши данные надёжно хранятся на вашем компьютере.
- Вы можете добавлять, редактировать, удалять записи в пару кликов.
- Вы можете с лёгкостью переносить данные в Excel\csv и обратно!

Перейдем к установке.
-----
Для начала скачайте установочный файл по этой [ссылке](https://github.com/AlexDev-py/Thermometry-Log/releases/tag/v1.1.0).

После запуска Вас поприветствует мастер установки и попросит нажать "Далее".
Сделайте это.

В следующем окне мастер попросит вас выбрать, какие компоненты необходимо установить.
В небольшом окошке будет всего 2 пункта **WebView2** и **Журнал термометрии**.
**WebView2** - необходимая для работы, утилита. 
Скорее всего, она не установлена на Вашем ПК, 
поэтому если вы устанавливаете приложение впервые, 
не убирайте этот компонент.
**Журнал термометрии** - то самое приложение, ради которого мы здесь собрались.
Когда вы выбрали, что устанавливать, нажмите на кнопку "Далее".

Следующим этапом будет выбор места, куда устанавливать приложение.
Вы можете выбрать любое удобное для вас место.

После нажатия на кнопку "Установить" запустится процесс установки. 
Это может занять некоторое время.

Когда все компоненты будут установлены,
мастер сообщит об этом. Нажмите на кнопку "Готово".

Для удобства мастер создает несколько ярлыков программы: 
один в меню Пуск, второй на рабочем столе.

После установки
----
Программа не требует каких-либо настроек после установки, 
поэтому вы можете сразу начинать работать.

Для разработчиков
----
_P.S.: Для запуска проекта необходим Python 3.8+ и Microsoft Edge [WebView2](https://developer.microsoft.com/en-us/microsoft-edge/webview2/#download-section)_ 

Вы можете скачать исходники проекта с помощью git.
```commandline
git clone https://github.com/AlexDev-py/Thermometry-Log.git
```

или загрузить архив, используя [ссылку](https://github.com/AlexDev-py/Thermometry-Log/archive/refs/heads/master.zip).

Далее вам необходимо создать виртуальное окружение 
и установить все зависимости проекта. Используйте это, находясь в директории проекта.
```commandline
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

Для запуска приложения из консоли необходимо выполнить это, находясь в директории проекта:
```commandline
venv\Scripts\activate.bat
cd ThermometryLog
python main.py
```
