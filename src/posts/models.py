from datetime import datetime
from uuid import UUID
from sqlalchemy import ForeignKey
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
    images: Mapped[list[FileModel]] = relationship("FileModel",
                                                   back_populates="post")

    # Отношение author:
    # - Связь с моделью User.
    # - back_populates указывает на атрибут posts в модели User,
    # который устанавливает обратное отношение.
    author: Mapped["User"] = relationship("User", back_populates="posts")

    # Связь с моделью Like.
    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post")

    # Связь с моделью Comment.
    comments: Mapped[list["Comment"]] = relationship("Comment",
                                                     back_populates="post")


class Like(Base):
    """Модель лайка."""
    __tablename__ = "likes"

    # Колонка user_id:
    # Тип данных int.
    # Внешний ключ, ссылающийся на колонку id таблицы 'users'.
    # Первичный ключ.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         primary_key=True)
    # Колонка post_id:
    # Тип данных int.
    # Внешний ключ, ссылающийся на колонку id таблицы 'posts'.
    # Первичный ключ.
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"),
                                         primary_key=True)
    # Отношение user:
    # Связь с моделью User.
    # back_populates указывает на атрибут likes в модели User,
    # который устанавливает обратное отношение.
    user: Mapped["User"] = relationship("User", back_populates="likes")

    # Отношение post:
    # Связь с моделью Post.
    # back_populates указывает на атрибут likes в модели Post,
    # который устанавливает обратное отношение.
    post: Mapped["Post"] = relationship("Post", back_populates="likes")


class Comment(Base):
    """Модель комментария."""
    __tablename__ = "comments"

    # Колонка id:
    # Тип данных int.
    # Первичный ключ.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Колонка user_id:
    # Тип данных int.
    # Внешний ключ, ссылающийся на колонку id таблицы 'users'.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Отношение user:
    # Связь с моделью User.
    # back_populates указывает на атрибут comments в модели User,
    # который устанавливает обратное отношение.
    user: Mapped["User"] = relationship("User", back_populates="comments")

    # Колонка post_id:
    # Тип данных int.
    # Внешний ключ, ссылающийся на колонку id таблицы 'posts'.
    # Индексированная колонка для улучшения производительности запросов.
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)

    # Отношение post:
    # Связь с моделью Post.
    # back_populates указывает на атрибут comments в модели Post,
    # который устанавливает обратное отношение.
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    content: Mapped[str]  # Содержимое комментария.

    created_at: Mapped[datetime]  # Дата и время создания комментария.
