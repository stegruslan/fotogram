# Fotogram_project

## Глава 1. ( Функционал)


1. Пользователь может зарегистрироваться.
2. Пользователь может сменить пароль.

3. Авторизация через JWT (JSON Web Tokens).
4. Пользователь может загружать фото с текстом.
5. Пользователь может добавлять в друзья.
6. Пользователь может писать комментарии к фотографиям.
7. Пользователь может смотреть список друзей.
8. Пользователь сможет смотреть ленту.
9. Поля пользователя:
- id
- username
- password (hash)
- fullname
- email
- avatar
- bio
---

Инструменты:
- Python
- FastAPI
- SQLAlchemy
---
![Текст с описанием картинки](https://github.com/stegruslan/fotogram/blob/master/image/Untitled%20Workspace.jpg)
---

**Grok** задаем порт ,который будет идти на движок **nginx**.
Если в адресе есть ручка с **API**, то **nginx** отправляет запрос на **backend**, 
если название домена без ручек, то на **frontend**

Установка окружения **poetry**:
```bash
poetry shell
poetry install
```

Инициализируем репозиторий:
```bash
git init
```
Установка **pre-commit** для чистоты ,наглядности и понятности кода:
```bash
pre-commit install
```
Добавляем вэб сервер **uvicorn**:
```bash
poetry add uvicorn
```



#### Папка src будет главной папкой проекта, из которой будем делать все запуски.

В файле **app.py** создаем пробный запуск приложения:
```bash
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
 запускаем тестируем в postman ( GET localhost:8000/)
Получаем:
{
    "Hello": "World"
}
```

