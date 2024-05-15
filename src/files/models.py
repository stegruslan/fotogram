from uuid import UUID

from sqlalchemy import text, ForeignKey
from sqlalchemy.types import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class FileModel(Base):
    __tablename__ = 'files'  # Имя таблицы в базе данных.

    # Колонка uuid:
    # - Тип данных UUID.
    # - Первичный ключ.
    # - Значение по умолчанию генерируется функцией gen_random_uuid().

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True,
                                       server_default=text(
                                           "gen_random_uuid()"))

    # Колонка extension:
    # - Тип данных строка.
    extension: Mapped[str]

    # Колонка post_id:
    # - Тип данных int.
    # - Внешний ключ, ссылающийся на колонку id таблицы 'posts'.
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    # Отношение posts:
    # - Связь с моделью Post.
    # - back_populates указывает на атрибут images в модели Post,
    # который устанавливает обратное отношение.
    posts: Mapped["Post"] = relationship("Post", back_populates="images")
