# Database-development

Это мой первый сайт с БД

Его идея заключается в том, чтобы делиться своим танцевальном творчеством с людьми, которых это тоже интересует.

Это версия инстаграмма на минималках

Как пользователь(таблица users), ты можешь:
- Сохранять в избранное понравившиеся танцы(ставить лайки) - максимум 1 лайк от 1го человека на запись(таблица - saved_publication)
- Комментировать чужие публикации - возможно много комментариев от одного пользователя под одной записью(таблица - Comments)
- Ну и конечно же публиковать свои танцы, так как в одном видео может быть сразу много пользователей этого сайта, 1 публикация может иметь много авторов, а 1 автор - много публикаций(publication_and_user) :)

Так как сайт про танцы, то танцоров очень часто может интересовать конкретный стиль, поэтому можно выбрать его и смотреть танцы других пользователей только в этом стиле, а про стили, которые можно выбрать в таблице - Styles

Все все публикации и их параметры - publications

Схема БД - [Schema.sql](https://github.com/Renata-2001/Database-development/blob/main/Schema.sql)

![](https://github.com/Renata-2001/Database-development/blob/main/Schema.png)

Для работы с БД используются функции из DanceDB.py
