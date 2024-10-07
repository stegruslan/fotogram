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

# Подключаем маршруты для управления пользователями,//
# постами и файлами с префиксом "/api/v1"
app.include_router(users_router, prefix="/api/v1", tags=["api/v1"])
app.include_router(posts_router, prefix="/api/v1", tags=["api/v1"])
app.include_router(files_router, prefix="/api/v1", tags=["api/v1"])


@app.get("/")
def read_root() -> dict[str, str]:
    """Тестовый эндпоинт.

    Returns
    -------
        dict[str, str]: тестовый словарь.

    """
    return {"Hello": "World"}
