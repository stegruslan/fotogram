"""Файл моделей ORM для части работы пользователей."""
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid
from database import Base
from uuid import UUID

from posts.models import Post


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"  # Имя таблицы в базе данных
    # Определение столбцов таблицы и их типов данных
    id: Mapped[int] = mapped_column(primary_key=True)
    # Уникальный идентификатор пользователя
    username: Mapped[str] = mapped_column(index=True, unique=True)
    # Имя пользователя
    fullname: Mapped[str]
    # Полное имя пользователя
    password: Mapped[str]
    # Хэшированный пароль пользователя
    birthday: Mapped[datetime | None]
    # День рождения пользователя (может быть None)
    bio: Mapped[str]  # Биография пользователя
    signup_at: Mapped[datetime]
    # Дата и время регистрации пользователя
    last_activity: Mapped[datetime]
    # Дата и время последней активности пользователя
    avatar: Mapped[str | None]  # Путь к аватару пользователя (может быть None)

    # Отношение с моделью Post.
    # Атрибут back_populates указывает на атрибут author в модели Post,
    # который устанавливает обратное отношение.
    posts: Mapped[list[Post]] = relationship("Post", back_populates="author")
