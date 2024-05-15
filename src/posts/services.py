from typing import Annotated

from fastapi import UploadFile, Form

from files.models import FileModel
from users.services import CurrentUser
from posts.schemas import PostSchema
from database import session_factory


async def create_post(current_user: CurrentUser,
                      content: Annotated[str, Form()],
                      file: UploadFile) -> None:
    with session_factory() as session:  # Создание сессии базы данных.
        extension = file.filename.split('.')[-1]  # Получение расширения файла.

        # Создание экземпляра FileModel с полученным расширением.
        file = FileModel(extension=extension)
        session.add(file)  # Добавление файла в сессию.
        session.flush()  # Выполнение команды flush для генерации UUID
        print(file.uuid)
        # with open("") as f:
        #     s = await file.read()
