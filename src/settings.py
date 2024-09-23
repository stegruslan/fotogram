"""Файл, хранящий глобальные настройки проекта."""
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс хранящий все настройки."""

    DB_DIALECT: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    PATH_FILES_STR: str = "./media_files"

    PATH_FILES: Path = Path(PATH_FILES_STR)

    class Config:
        """Конфиг настроек."""

        case_sensitive = True
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()
