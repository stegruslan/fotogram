from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from users.schemas import UserSchema


# Определение схемы данных для поста.
class PostSchema(BaseModel):
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
    posts: list[PostSchema]


# Определение схемы данных для входящего комментария
class CommentInputSchema(BaseModel):
    content: str


# Определение схемы данных для комментария.
class CommentSchema(BaseModel):
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime


class CommentWithUserSchema(BaseModel):
    id: int  # ID комментария.
    user: UserSchema  # Информация о пользователе, оставившем комментарий.
    post_id: int  # ID поста, к которому относится комментарий.
    content: str  # Содержимое комментария.
    created_at: datetime  # Дата и время создания комментария.
    owner: bool  # Является ли текущий пользователь автором комментария.


# Определение схемы данных для ответа, содержащего список комментариев.
class CommentsOutputSchema(BaseModel):
    comments: list[
        CommentWithUserSchema]  # Список комментариев с информацией о пользователе.
