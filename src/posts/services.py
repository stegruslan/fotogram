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
    with session_factory() as session:
        post = Post(content=content, created_at=datetime.now(),
                    author=current_user)
        session.add(post)
        session.flush()
        for file in files:
            ext = file.filename.split('.')[-1]
            file_uuid = uuid.uuid4()
            file_path = settings.PATH_FILES / (str(file_uuid) + "." + ext)
            file_bytes = await file.read()
            with file_path.open(mode='wb') as f:
                f.write(file_bytes)
            file_model = FileModel(uuid=file_uuid, extension=ext,
                                   post_id=post.id)
            session.add(file_model)
        session.commit()
