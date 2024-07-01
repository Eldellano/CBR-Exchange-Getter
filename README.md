## CBR-Exchange-Getter
---

#### Сервис созданный для получения данных о стоимости валют через api сайта cbr.ru.

### Взаимодействие с сервисом

Раз в сутки сервис делает запрос к api, сохраняет результаты в базу данных. 
Через эндпоинт /get_exchange можно запросить данные о стоимости валюты. 

---
Для реализации использованы:

Python 3.11

FastApi - для создания api интерфейса сервиса.

Celery - для создания очередей задач.

Celery Beat - для выполнения запроса к api по расписанию.

PostgreSQL - для хранения данных.


---

### Методы api сервиса:

* `/get_exchange?num_code=036&char_code=AUD&date_req=30.06.2024` - GET запрос для получения стоимости валюты, 
сохраненной в базе данных. 
num_code - номер валюты, char_code - код валюты, date_req - дата на которую необходимо получить 
стоимость валюты из базы данных.
Обязательным является передача num_code либо char_code. date_req - необязательный параметр, 
без его указания будет выгружена стоимость валюты в день запроса.

    ##### Примеры запросов: 
  * `http://127.0.0.1:5000/get_exchange?num_code=036&date_req=30.06.2024`
  * `http://127.0.0.1:5000/get_exchange?char_code=AUD&date_req=30.06.2024`
  * `http://127.0.0.1:5000/get_exchange?char_code=AUD`  

  ##### Возможные варианты ответа:
  * При успешной получении данных из базы, будет возвращена информация о запрошенной валюте - "{\"name\": \"Австралийский доллар\", \"num_code\": \"036\", \"char_code\": \"AUD\", \"value\": 56.7995, \"vunit_retention\": 56.7995, \"request_date\": \"30.06.2024\"}".
  * Если не переданы параметры `num_code` и `char_code` будет возвращено сообщение "В запросе должен быть указан num_code или char_code".
  * Если на указанную дату нет данных о стоимости валюты будет возвращено сообщение - "Данные по валюте за {дата} отсутствуют".

---

### Мониторинг задач Flower

Мониторинг доступен по адресу http://127.0.0.1:5555/flower/

Мониторинг может отображать статусы задач - в ожидании, готово и не выполнено,
а так же запущенные воркеры.

Для каждой задачи доступно подробное описание - время добавления задачи, время старта и время завершения.
В случае не выполнения задачи можно проверить из-за какой ошибки произошел сбой.


---

### Сборка в Docker:

1. Переименовать файл .env.example в .env
2. В файле .env указать необходимы порты сервиса.
3. При необходимости в файле .env поменять порты сервиса, время для запроса. 
3. Находясь в папке с проектом собрать сервис командой ```docker-compose up -d```
4. После запуска сервис будет доступен по адресу `http://127.0.0.1:port_from_env`

---
