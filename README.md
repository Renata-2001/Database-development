# Database-development

### Начнем с описания самой БД\
![image](https://github.com/Renata-2001/Database-development/assets/93085543/a4140f7e-2734-4caf-ad50-067f46898ead)


\\
У нас есть 5 таблиц:
Клиент: Клиент записывается через сайт, он может выбрать время, услугу и мастера. Также клиенту необходимо указать контактные данные для связи с ним и подтверждения записи.\

Мастер: У него есть фиксированное окно времени, в которое он может принимать клиентов, и набор услуг, которые он может оказать.\

Услуги: Услуги оказываются в примерно указанное время, клиент может не толко выбрать набор услуг, но и понять, сколько примерно по времени он на них потратит. Еще нужно для понимания оставшегося свободного времени у мастера.\

Навыки: Не все мастера могут делать весь набор услуг. Это таблица связи для понимания, кого из специалистов можно выбрать для оказания конкретной услуги\

Запись: Таблица записей содержит все записи. по которым можно понять в какое время, кто, кому и какую услугу оказывает\

График работы: Мастера заранее выбирают себе график работы(на месяц вперед, отмечают интервалы времени, в которые могут работать)\

