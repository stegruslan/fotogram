from fastapi import HTTPException
from starlette.responses import FileResponse

from database import session_factory
from files.models import FileModel
from settings import settings


def get_file(filename: str) -> FileResponse:
    with session_factory() as session:
        try:
            file_uuid, ext = filename.rsplit('.', 1)
            file_model = session.query(FileModel).filter(
                FileModel.uuid == file_uuid).first()
            if not file_model or file_model.extension != ext:
                raise HTTPException(status_code=404,
                                    detail=f'File {file_uuid} is not found')
            return FileResponse(path=settings.PATH_FILES / filename,
                                filename=filename)
        except ValueError as e:
            raise HTTPException(status_code=404, detail='Bad filename')
