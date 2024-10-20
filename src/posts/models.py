from datetime import datetime

from sqlalchemy import text, ForeignKey, Column, Integer

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from files.models import FileModel


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str | None]
    created_at: Mapped[datetime]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    images: Mapped[list[FileModel]] = relationship("FileModel",
                                                   back_populates="post")

    author: Mapped["User"] = relationship("User", back_populates="posts")

    likes: Mapped[list["Like"]] = relationship("Like", back_populates="post")

    comments: Mapped[list["Comment"]] = relationship("Comment",
                                                     back_populates="post")


class Like(Base):
    """Модель лайка."""
    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),
                                         primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"),
                                         primary_key=True)
    user: Mapped["User"] = relationship("User", back_populates="likes")
    post: Mapped["Post"] = relationship("Post", back_populates="likes")


class Comment(Base):
    """Модель комментария."""
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), index=True)
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    content: Mapped[str]
    created_at: Mapped[datetime]
