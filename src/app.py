"""Модуль для запуска FASTAPI."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """Тестовый эндпоинт.

    Returns
    -------
        dict[str, str]: тестовый словарь.

    """
    return {"Hello": "World"}
