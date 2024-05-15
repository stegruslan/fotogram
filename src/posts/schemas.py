from datetime import datetime

from pydantic import BaseModel


# Определение схемы данных для поста.
class PostSchema(BaseModel):
    id: int  # ID поста.
    filename: str  # Имя файла, связанного с постом.
    content: str  # Содержимое поста.
    author_id: int  # ID автора поста.
    author_name: str  # Имя автора поста.
    created_at: datetime  # Дата и время создания поста.
