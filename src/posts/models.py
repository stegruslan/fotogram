from datetime import datetime
from uuid import UUID

from sqlalchemy import text, ForeignKey
from sqlalchemy.types import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from files.models import FileModel


class Post(Base):
    __tablename__ = "posts"  # Имя таблицы в базе данных.

    # Колонка id:
    # - Тип данных int.
    # - Первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Колонка content:
    # - Тип данных строка или None (может быть пустой).
    content: Mapped[str | None]

    # Колонка created_at:
    # - Тип данных datetime.
    created_at: Mapped[datetime]

    # Колонка author_id:
    # - Тип данных int.
    # - Внешний ключ, ссылающийся на колонку id таблицы 'users'.
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Отношение images:
    # - Связь с моделью FileModel.
    # - back_populates указывает на атрибут posts в модели FileModel,
    # который устанавливает обратное отношение.
    images: Mapped[list[FileModel]] = relationship("FileModel", back_populates="posts")

    # Отношение author:
    # - Связь с моделью User.
    # - back_populates указывает на атрибут posts в модели User,
    # который устанавливает обратное отношение.
    author: Mapped["User"] = relationship("User", back_populates="posts")
