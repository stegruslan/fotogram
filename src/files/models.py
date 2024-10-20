from uuid import UUID

from sqlalchemy import text, ForeignKey
from sqlalchemy.types import Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class FileModel(Base):
    __tablename__ = 'media_files'

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True,
                                       server_default=text(
                                           "gen_random_uuid()"))

    extension: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))
    post: Mapped['Post'] = relationship("Post", back_populates="images")

    def get_filename(self) -> str:
        return f"{self.uuid}.{self.extension}"
