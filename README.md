# Fotogram_project

## Глава 1. ( Функционал)


1. Пользователь может зарегистрироваться.
2. Пользователь может сменить пароль.

3. Авторизация через JWT.
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



Гроку задаем порт который будет идти на движок инджинкс
Если в адресе есть ручка с АПИ то Нджинкс кидает на бэк, 
если просто название домена без ручек, то на ФРОНТ

Установка окружения poetry
poetry shell
poetry install

Инициализируем репозиторий
git init

и установим прикомит для чистоты ,наглядности и понятности кода
pre-commit install
Добавим вэб сервер ювикорн
poetry add uvicorn



Папка src будет главной папкой проекта, из которой будем делать все запуски

в файле app.py создаем пробный запуск приложения

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
 Работает!
