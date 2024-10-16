# DanceConnect

Это мой первый сайт с БД

Его идея заключается в том, чтобы делиться своим танцевальном творчеством с людьми, которых это тоже интересует.

Это версия инстаграмма на минималках

Как пользователь(таблица users), ты можешь:

- Сохранять в избранное понравившиеся танцы(ставить лайки) - максимум 1 лайк от 1го человека на запись(таблица - saved_publication)
- Комментировать чужие публикации - возможно много комментариев от одного пользователя под одной записью(таблица - comment_public)
- Подписываться на других людей(таблица - followers)

Так как сайт про танцы, то танцоров очень часто может интересовать конкретный стиль, поэтому можно выбрать его и смотреть танцы других пользователей только в этом стиле, а про стили, которые можно выбрать в таблице - Styles

Все все публикации и их параметры - publications

Схема БД - [Schema.sql](https://github.com/Renata-2001/Database-development/blob/main/Schema.sql)

![](https://github.com/Renata-2001/Database-development/blob/main/Schema.png)

## Инструкция по развертыванию приложения

### Установка всех необходимых пакетов

```
$ apt-get update
$ apt install python3-psycopg2
$ apt install python3-flask
$ apt install python3-flask-login
$ apt install postgresql
```

### Подготовка сервера

Создаем базу данных postgres, где

- rolename - учетная запись

- dbname - название БД

- passwd - пароль от БД

```
$ sudo -i -u postgres psql
# CREATE USER rolename;
# \password rolename
# CREATE DATABASE dbname;
# ALTER DATABASE dbname OWNER TO rolename;
# quit;
```

### Конфигурация приложения

Файл конфигурации - FLASK_CONFIGURATION_SETUP:

```
MEDIA_PATH = "path/application/static/video"
VIDEO_PATH = "/static/video"
SECRET_KEY = 'secret_key'
DATABASE = 'dbname'
USERNAME ='rolename' 
PASSWORD = 'passwd'
HOST = '0.0.0.0'
PORT = '8000'
DEBUG = True
```

- Зайдите в директорию, где хранятся файлы вашего приложения

- Задайте переменную среды CONFIG, указав в ней путь к FLASK_CONFIGURATION_SETUP

- Загрузите схему в БД

```
$ export CONFIG='/path/to/config/file'
$ psql -U USER -d dbname 
# \i schema.sql
```

### Запуск приложения

Необходимо создать папку video внутри path/application/static, где будут храниться видео пользователей

Выполните комманду:

```
$ python3 app.py
```
