from datetime import datetime

from pydantic import BaseModel


# Определение схемы данных для поста.
class PostSchema(BaseModel):
    id: int  # ID поста.
    images: list[str]  # Имя файла, связанного с постом.
    content: str  # Содержимое поста.
    author_id: int  # ID автора поста.
    author_name: str  # Имя автора поста.
    created_at: datetime  # Дата и время создания поста.


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
