"""Маршруты для пользователей."""
from fastapi import APIRouter

import users.schemas
from users import schemas
from users.schemas import UserSchema, Token, MessageCreate, MessageResponse
from users.services import signup, login_for_access_token, read_users_me, \
    send_message, get_messages
from users.services import login_for_access_token, read_users_me, signup, \
    subscribe, unsubscribe

router = APIRouter(prefix="/users", tags=["users"])
router.post("/signup/", response_model=UserSchema)(signup)
# Маршрут для регистрации нового пользователя (/users/signup/)
# С указанием модели данных,
# которая будет возвращена в ответ на запрос (UserSchema)

router.post("/login/", response_model=Token)(login_for_access_token)
# Регистрация маршрута для аутентификации пользователя (/users/login/)
# с указанием модели данных, которая будет возвращена в ответ на запрос (Token)

router.get("/test/")(read_users_me)
# Маршрут для получения информации о текущем пользователе.
# Путь '/test/' будет добавлен к префиксу
# '/users', что дает полный путь '/users/test/'.
# Функция read_users_me будет вызываться при обращении к этому пути.

router.post("/{author_id}/subscribe/")(subscribe)
# Маршрут для подписки на автора (/users/{author_id}/subscribe/)
# Функция subscribe будет вызываться при обращении к этому пути.

router.post("/{author_id}/unsubscribe/")(unsubscribe)
# Маршрут для отписки от автора (/users/{author_id}/unsubscribe/)
# Функция unsubscribe будет вызываться при обращении к этому пути.

router.post("/messages/", response_model=MessageResponse)(
    send_message)

router.get("/messages/", response_model=MessageResponse)(
    get_messages)
