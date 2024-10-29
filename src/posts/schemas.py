from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from users.schemas import UserSchema


class PostSchema(BaseModel):
    """Схема данных для поста."""
    id: int
    images: list[str]
    content: str
    author_id: int
    author_name: str
    created_at: datetime
    count_likes: int
    liked: bool
    count_comments: int
    is_subscribed: Optional[bool] = None


class ResponsePostsSchema(BaseModel):
    """Схема ответа, содержащая список постов."""
    posts: list[PostSchema]


class CommentInputSchema(BaseModel):
    """Схема для входящего комментария."""
    content: str


class CommentSchema(BaseModel):
    """Схема данных для комментария."""

    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime


class CommentWithUserSchema(BaseModel):
    """Схема данных для комментария с информацией о пользователе."""
    id: int  # ID комментария.
    user: UserSchema  # Информация о пользователе, оставившем комментарий.
    post_id: int  # ID поста, к которому относится комментарий.
    content: str  # Содержимое комментария.
    created_at: datetime  # Дата и время создания комментария.
    owner: bool  # Является ли текущий пользователь автором комментария.


class CommentsOutputSchema(BaseModel):
    """Схема ответа, содержащая список комментариев с информацией о пользователе."""
    comments: list[
        CommentWithUserSchema]
