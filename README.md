# Friend+
Документация по сервису "Friend+"
Запуск сервиса
Установите все зависимости, указанные в файле requirements.txt, с помощью команды:

```pip install -r requirements.txt```

Создайте и примените миграции базы данных с помощью следующих команд:

```python manage.py makemigrations
python manage.py migrate
```
Запустите сервер разработки Django с помощью команды:

```python manage.py runserver```

Сервер будет запущен по адресу http://localhost:8000/.

API Endpoint's
Регистрация нового пользователя
URL: /api/users/

Метод: POST

Тело запроса:

```
{
  "username": "john_doe",
  "password": "password123"
}
```

Пример успешного ответа:

```
{
  "id": 1,
  "username": "john_doe"
}
```

Отправка заявки в друзья
URL: /api/friend-requests/

Метод: POST

Тело запроса:

```
{
  "from_user": 1,
  "to_user": 2
}
```

Пример успешного ответа:

```
{
  "id": 1,
  "from_user": {
    "id": 1,
    "username": "john_doe"
  },
  "to_user": {
    "id": 2,
    "username": "jane_smith"
  },
  "created_at": "2023-05-10T12:00:00Z"
}
```

Принятие заявки в друзья
URL: /api/friend-requests/{friend_request_id}/accept/

Метод: POST

Пример успешного ответа:

```
{
  "message": "Friend request accepted"
}
```

Отклонение заявки в друзья
URL: /api/friend-requests/{friend_request_id}/reject/

Метод: POST

Пример успешного ответа:

```
{
  "message": "Friend request rejected"
}
```

Просмотр списка входящих заявок в друзья
URL: /api/friend-requests/incoming/

Метод: GET

Пример успешного ответа:

```
[
  {
    "id": 1,
    "from_user": {
      "id": 2,
      "username": "jane_smith"
    },
    "to_user": {
      "id": 1,
      "username": "john_doe"
    },
    "created_at": "2023-05-10T12:00:00Z"
  }
]
```

Просмотр списка исходящих заявок в друзья
URL: /api/friend-requests/outgoing/

Метод: GET

Пример успешного ответа:

```
[
  {
    "id": 2,
    "from_user": {
      "id": 1,
      "username": "john_doe"
    },
    "to_user": {
      "id": 3,
      "username": "mark_jackson"
    },
    "created_at": "2023-05-11T09:30:00Z"
  }
]
```

Просмотр списка друзей
URL: /api/friends/

Метод: GET

Пример успешного ответа:

```
[
  {
    "id": 1,
    "users": [
      {
        "id": 1,
        "username": "john_doe"
      },
      {
        "id": 2,
        "username": "jane_smith"
      }
    ],
    "created_at": "2023-05-10T15:45:00Z"
  },
  {
    "id": 2,
    "users": [
      {
        "id": 1,
        "username": "john_doe"
      },
      {
        "id": 3,
        "username": "mark_jackson"
      }
    ],
    "created_at": "2023-05-11T10:15:00Z"
  }
]
```

Просмотр статуса дружбы
URL: /api/friends/status/{user_id}/

Метод: GET

Пример успешного ответа:

```
{
  "status": "friends"
}
```

Удаление друга
URL: /api/friends/{friend_id}/remove/

Метод: POST

Пример успешного ответа:

```
{
  "message": "Friend removed"
}
```

Завершение работы с сервисом
Для остановки сервера разработки Django, нажмите Ctrl + C или Ctrl + Break в командной строке.
