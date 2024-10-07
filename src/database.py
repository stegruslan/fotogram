"""Файл для описания объекта sqlalchemy базы данных."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import settings

# Создание соединения с базой данных SQLAlchemy
engine = create_engine(
    f"postgresql+psycopg2://"
    f"{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)


session_factory = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Базовая модель."""
