from datetime import datetime

from pydantic import BaseModel

from users.schemas import UserSchema


# Определение схемы данных для поста.
class PostSchema(BaseModel):
    id: int  # ID поста.
    images: list[str]  # Имя файла, связанного с постом.
    content: str  # Содержимое поста.
    author_id: int  # ID автора поста.
    author_name: str  # Имя автора поста.
    created_at: datetime  # Дата и время создания поста.
    count_likes: int  # Кол-во лайков
    liked: bool
    count_comments: int


class ResponsePostsSchema(BaseModel):
    posts: list[PostSchema]


# Определение схемы данных для входящего комментария.
class CommentInputSchema(BaseModel):
    content: str


# Определение схемы данных для комментария.
class CommentSchema(BaseModel):
    id: int  # ID комментария.
    user_id: int  # ID пользователя, который оставил комментарий.
    post_id: int  # ID поста, к которому относится комментарий.
    content: str  # Содержимое комментария.
    created_at: datetime  # Дата и время создания комментария.


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
