"""Маршруты для пользователей."""
from typing import List
from fastapi import APIRouter
import users.schemas
from users import schemas
from users.schemas import UserSchema, Token, MessageCreate, MessageResponse
from users.services import signup, login_for_access_token, read_users_me, \
    send_message, get_messages, open_get_send_chat, get_all_chats, \
    get_user_name
from users.services import login_for_access_token, read_users_me, signup, \
    subscribe, unsubscribe

router = APIRouter(prefix="/users", tags=["users"])
router.post("/signup/", response_model=UserSchema)(signup)
# Маршрут для регистрации нового пользователя.


router.post("/login/", response_model=Token)(login_for_access_token)
# Регистрация маршрута для аутентификации пользователя.
# с указанием модели данных, которая будет возвращена в ответ на запрос (Token)

router.get("/test/")(read_users_me)
# Маршрут для получения информации о текущем пользователе.


router.post("/{author_id}/subscribe/")(subscribe)
# Маршрут для подписки на автора.


router.post("/{author_id}/unsubscribe/")(unsubscribe)
# Маршрут для отписки от автора.


router.post("/messages/", response_model=MessageResponse)(
    send_message)
# # Маршрут для отправки сообщения от текущего пользователя другому пользователю.

router.get("/messages/", response_model=List[MessageResponse])(
    get_messages)
# Возвращает все сообщения, в которых участвует текущий пользователь.

router.post("/chat/", response_model=list[schemas.MessageResponse])(
    open_get_send_chat)
# Получает историю сообщений между текущим пользователем и указанным получателем.
# Если история пуста, отправляет новое сообщение, если указано содержимое.


router.get("/chats/")(get_all_chats)
# Возвращает последние сообщения из всех чатов, в которых участвует текущий пользователь


router.get("/chats/{user_id}", response_model=UserSchema)(get_user_name)
# Возвращает информацию о пользователе по его ID

