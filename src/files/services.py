from fastapi import HTTPException
from starlette.responses import FileResponse

from database import session_factory
from files.models import FileModel
from settings import settings


def get_file(filename: str) -> FileResponse:
    # Принимает имя файла и возвращает FileResponse
    with session_factory() as session:
        # Создает сессию для взаимодействия с базой данных
        try:
            file_uuid, ext = filename.rsplit('.', 1)
            # Разделяет имя файла на UUID и расширение
            file_model = session.query(FileModel).filter(
                FileModel.uuid == file_uuid).first()
            # Ищет файл в базе данных по UUID
            if not file_model or file_model.extension != ext:
                # Проверяет, существует ли файл и совпадает ли расширение
                raise HTTPException(status_code=404,
                                    detail=f'File {file_uuid} is not found')
            # Если файл не найден или расширение не совпадает,
            # выбрасывает исключение
            return FileResponse(path=settings.PATH_FILES / filename,
                                filename=filename)
        # Если файл найден и расширение совпадает, возвращает файл в ответе
        except ValueError as e:
            raise HTTPException(status_code=404, detail='Bad filename')
            # Вызывает исключение HTTP 404, если формат имени файла неверный
