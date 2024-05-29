import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy.orm import selectinload

from posts.models import Like, Post, Comment
from posts.schemas import CommentInputSchema, CommentSchema
from fastapi import Form, UploadFile
from starlette.responses import Response
from fastapi import Form, UploadFile, HTTPException
from database import session_factory
from files.models import FileModel
from posts.models import Like, Post, Comment
from settings import settings
from users.services import CurrentUser
from posts.schemas import CommentInputSchema, CommentSchema, PostSchema, \
    ResponsePostsSchema


def get_posts(current_user: CurrentUser) -> ResponsePostsSchema:
    with session_factory() as session:
        posts = session.query(Post).options(selectinload(Post.images),
                                            selectinload(Post.author)).all()
        posts_schemas = [
            PostSchema(
                id=post.id,
                images=list(
                    map(lambda x: x.get_filename(), post.images)),
                content=post.content,
                author_id=post.author.id,
                author_name=post.author.fullname,
                created_at=post.created_at,
            )
            for post in posts
        ]
        return ResponsePostsSchema(posts=posts_schemas)


async def create_post(current_user: CurrentUser,
                      content: Annotated[str, Form()],
                      files: list[UploadFile]) -> None:
    """
       Создает новый пост с файлами.

       Args:
           current_user (CurrentUser): Текущий пользователь.
           content (str): Содержимое поста.
           files (list[UploadFile]): Список файлов для загрузки.

       Returns:
           None
       """

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


def like_post(current_user: CurrentUser, post_id: int, like: bool) -> Response:
    """
        Обрабатывает лайк или дизлайк поста.

        Args:
            current_user (CurrentUser): Текущий пользователь.
            post_id (int): ID поста.
            like (bool): True для лайка, False для удаления лайка.

        Returns:
            Response: HTTP-ответ.
        """
    with session_factory() as session:
        # Создаем сессию для взаимодействия с базой данных.
        user_like = session.query(Like,
                                  ).filter(
            Like.post_id == post_id,
            Like.user_id == current_user.id,
        ).first()
        # Ищем существующий лайк пользователя для данного поста.
        if like and user_like or not like and not user_like:
            # Если лайк уже существует или дизлайк уже отсутствует,
            # возвращаем статус 200.
            return Response(status_code=200)
        if not user_like:
            # Если лайка нет, создаем новый лайк.
            user_like = Like(post_id=post_id, user_id=current_user.id)
            session.add(user_like)
            session.commit()
            return Response(status_code=200)
        if user_like:
            # Если лайк есть, удаляем его.
            session.delete(user_like)
            session.commit()
            return Response(status_code=200)


def create_comment(current_user: CurrentUser, post_id: int,
                   comment: CommentInputSchema) -> CommentSchema:
    """
        Создает новый комментарий к посту.

        Args:
            current_user (CurrentUser): Текущий пользователь.
            post_id (int): ID поста.
            comment (CommentInputSchema): Данные комментария.

        Returns:
            CommentSchema: Созданный комментарий.
        """
    with session_factory() as session:
        # Создаем сессию для взаимодействия с базой данных.
        user_comment = Comment(
            user=current_user,
            post_id=post_id,
            content=comment.content,
            created_at=datetime.now(),
        )
        # Создаем объект комментария с данными из входной схемы.
        session.add(user_comment)
        # Добавляем комментарий в сессию.
        session.commit()
        # Коммитим изменения в базу данных.
        return CommentSchema(
            id=user_comment.id,
            content=user_comment.content,
            created_at=user_comment.created_at,
            user_id=user_comment.user_id,
            post_id=user_comment.post_id
        )
    # Возвращаем данные созданного комментария.


def delete_comment(current_user: CurrentUser, post_id: int,
                   comment_id: int) -> Response:
    """
        Удаляет комментарий к посту.

        Args:
            current_user (CurrentUser): Текущий пользователь.
            post_id (int): ID поста.
            comment_id (int): ID комментария.

        Returns:
            Response: HTTP-ответ.
        """
    with session_factory() as session:
        # Создаем сессию для взаимодействия с базой данных.
        comment = session.query(Comment).filter(
            Comment.id == comment_id).filter(
            Comment.post_id == post_id
        ).first()
        # Ищем комментарий по идентификатору и идентификатору поста.
        if not comment:
            # Если комментарий не найден, возвращаем ошибку 404.
            raise HTTPException(status_code=404,
                                detail=f"Comment with id {comment_id} not found")
        if comment.user_id != current_user.id:
            # Если текущий пользователь не является автором комментария,
            # возвращаем ошибку 403.
            raise HTTPException(status_code=403,
                                detail="You are not permission to delete this comment")
        session.delete(comment)
        # Удаляем комментарий из базы данных.
        session.commit()
        # Коммитим изменения.
        return Response(status_code=204)
    # Возвращаем ответ с кодом 204 (No Content).
