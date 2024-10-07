from uuid import UUID

from sqlalchemy import text, ForeignKey
from sqlalchemy.types import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class FileModel(Base):
    __tablename__ = 'media_files'  # Имя таблицы в базе данных

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
    post: Mapped['Post'] = relationship("Post", back_populates="images")

    def get_filename(self) -> str:
        return f"{self.uuid}.{self.extension}"
