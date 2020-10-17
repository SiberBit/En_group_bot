# En+ group bot
#### Чат бот в котором можно найти ответы на часто задаваемые вопросы

## Настройка окружения проекта:
1. Склонировать к себе репозиторий проекта
    ```linux
    $ git clone https://github.com/SiberBit/En_group_bot.git  
    ```
2. Находясь в папке проекта, создать виртуальное окружение
    ```linux
    $ python -m venv venv  
    ```
3. Активировать виртуальное окружение:
    - для Linux
        ```linux
        $ source venv/bin/activate  
        ```
      
    - для Windows
        ```windows
        $ venv\Scripts\activate.bat 
        ```
4. Установить зависимости (пакеты)
    ```linux
    (venv) $ pip install -r requirements.txt
    ```
5. Создать файл ```En_group_bot/.env``` с переменными окружения
```.env
DEBUG=
SECRET_KEY=
DATABASE_URL=
SQLITE_URL=
TG_TOKEN=
```

## Запуск сервера локально
```linux
$ python manage.py runserver
```

## Запуск telegram бота локально
```linux
$ python manage.py start_tg_bot
```