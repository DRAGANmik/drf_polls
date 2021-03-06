# drf_polls

# API для системы опросов пользователей

Функционал для администратора системы:

- авторизация в системе
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (endpoint ../users/me/)

## Технологии и требования:
```
Python 3.8+
Django 2.2.10
Django REST Framework
Docker
PostgreSQL
Poetry
```


## Запуск проекта в Docker окружении 

- Запустить проект: 
    ```shell
    docker-compose up --build
     ```
- Запустить проект в автономном режиме: 
    ```shell
    docker-compose up -d --build
     ```
- Применить миграции:
   ```shell
   docker-compose exec web python manage.py migrate --noinput
   ```
- Создать суперпользователя:
  ```shell
  docker-compose exec web python manage.py createsuperuser
    ```
- Остановить проект сохранив данные в БД:
    ```shell
    docker-compose down
    ```
- Остановить проект удалив данные в БД:
    ```shell
    docker-compose down --volumes
    ```
  
## Документация: 
## - http://127.0.0.1:8000/swagger/
## - http://127.0.0.1:8000/redoc/