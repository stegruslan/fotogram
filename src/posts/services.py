import uuid
from datetime import datetime
from pathlib import Path
from typing import Annotated

from fastapi import UploadFile, Form

from files.models import FileModel
from posts.models import Post
from settings import settings
from users.services import CurrentUser
from posts.schemas import PostSchema
from database import session_factory


async def create_post(current_user: CurrentUser,
                      content: Annotated[str, Form()],
                      files: list[UploadFile]) -> None:
    # Определяет асинхронную функцию create_post,
    # которая принимает текущего пользователя,
    # содержимое поста и список файлов для загрузки, и возвращает None
    with session_factory() as session:
        # Создается сессия для взаимодействия с базой данных
        post = Post(content=content, created_at=datetime.now(),
                    author=current_user)
        # Создает объект поста с содержимым, текущей датой и автором
        session.add(post)
        # Добавляет пост в сессию
        session.flush()
        # Сбрасывает изменения, чтобы получить идентификатор поста
        for file in files:
            # Итерирует по каждому файлу в списке файлов
            ext = file.filename.split('.')[-1]
            # Извлекает расширение файла
            file_uuid = uuid.uuid4()
            # Генерирует уникальный идентификатор для файла
            file_path = settings.PATH_FILES / (str(file_uuid) + "." + ext)
            # Формирует путь к файлу,
            # подставляя путь из настроек
            # с уникальным идентификатором и расширением
            file_bytes = await file.read()
            # Асинхронно читает содержимое файла
            with file_path.open(mode='wb') as f:
                f.write(file_bytes)
                # Открывает файл для записи в бинарном режиме
                # и записывает содержимое
            file_model = FileModel(uuid=file_uuid, extension=ext,
                                   post_id=post.id)
            # Создает объект FileModel с UUID, расширением
            # и идентификатором поста
            session.add(file_model)
            # Добавляет файл в сессию
        session.commit()
        # Коммитит все изменения в базе данных
