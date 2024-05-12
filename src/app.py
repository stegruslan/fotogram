"""Модуль для запуска FASTAPI."""
from fastapi import FastAPI

from users.routing import router as users_router

app = FastAPI()
app.include_router(users_router, prefix="/api/v1", tags=["api/v1"])
app.include_router(users_router, prefix="/api/v2", tags=["api/v2"])


@app.get("/")
def read_root() -> dict[str, str]:
    """Тестовый эндпоинт.

    Returns
    -------
        dict[str, str]: тестовый словарь.

    """
    return {"Hello": "World"}
