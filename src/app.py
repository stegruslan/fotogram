"""Модуль для запуска FASTAPI."""
from datetime import datetime
from http.client import HTTPException

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from database import session_factory
from files.routing import router as files_router
from posts.routing import router as posts_router
from settings import settings
from users.models import User, Subscribe, Message
from users.routing import router as users_router
from users.services import get_current_user


def create_app() -> FastAPI:
    # Если директория для файлов не существует, создаем её
    if not settings.PATH_FILES.is_dir():
        settings.PATH_FILES.mkdir()
    fastapi_app = FastAPI()
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return fastapi_app


app = create_app()

# Подключаем маршруты для управления пользователями,
# постами и файлами с префиксом "/api/v1"
app.include_router(users_router, prefix="/api/v1", tags=["api/v1"])
app.include_router(posts_router, prefix="/api/v1", tags=["api/v1"])
app.include_router(files_router, prefix="/api/v1", tags=["api/v1"])


# @app.websocket("/ws/chat/{receiver_id}")
#
#
# async def chat_websocket(
#     websocket: WebSocket,
#     receiver_id: int,
#     current_user: User = Depends(get_current_user)
# ):
#     await websocket.accept()  # Подключаем WebSocket
#
#     with session_factory() as session:
#         # Проверяем, подписаны ли текущий пользователь и получатель друг на друга
#         subscription = session.query(Subscribe).filter_by(
#             subscriber_id=current_user.id,
#             author_id=receiver_id
#         ).first()
#
#         if not subscription:
#             await websocket.close(
#                 code=1008)  # Закрываем соединение, если пользователи не подписаны друг на друга
#             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                                 detail="You are not subscribed to this user.")
#
#         try:
#             while True:
#                 data = await websocket.receive_text()  # Получаем сообщение от пользователя
#
#                 # Сохраняем сообщение в базе данных
#                 message = Message(
#                     sender_id=current_user.id,
#                     receiver_id=receiver_id,
#                     content=data,
#                     timestamp=datetime.utcnow()
#                 )
#                 session.add(message)
#                 session.commit()
#
#                 # Отправляем подтверждение отправителю
#                 await websocket.send_text(f"Message sent: {data}")
#
#         except WebSocketDisconnect:
#             await websocket.close()  # Закрываем WebSocket при отключении клиента
#

@app.get("/")
def read_root() -> dict[str, str]:
    """Тестовый эндпоинт.

    Returns
    -------
        dict[str, str]: тестовый словарь.

    """
    return {"Hello": "World"}
