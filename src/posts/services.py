import uuid
from datetime import datetime
from typing import Annotated, Optional
import logging
from fastapi import Form, UploadFile, HTTPException, Depends
from sqlalchemy.orm import selectinload
from starlette.responses import Response
from users.models import Subscribe
from database import session_factory
from files.models import FileModel
from posts.models import Like, Post, Comment
from posts.schemas import CommentInputSchema, CommentSchema, PostSchema, \
    ResponsePostsSchema, CommentWithUserSchema, CommentsOutputSchema
from settings import settings
from users.models import User
from users.schemas import UserSchema
from users.services import CurrentUser, get_current_user, oauth2_scheme

MAX_FILE_SIZE = 6 * 1024 * 1024  # Максимальный размер файла  6 МБ


def get_posts_subscribes(current_user: CurrentUser,
                         user_id: int | None = None) -> ResponsePostsSchema:
    """
    Получает посты только от пользователей, на которых подписан текущий пользователь.

    Args:
        current_user (CurrentUser): Текущий пользователь.
        user_id (int | None): ID пользователя, чьи посты нужно получить (если указан).

    Returns:
        ResponsePostsSchema: Схема с информацией о постах.
    """
    with session_factory() as session:
        # Получаем IDs пользователей, на которых подписан текущий пользователь
        subscribed_users_ids = session.query(Subscribe.author_id).filter(
            Subscribe.subscriber_id == current_user.id
        ).subquery()

        # Запрос постов от пользователей, на которых подписан текущий пользователь
        query = session.query(Post).filter(
            Post.author_id.in_(subscribed_users_ids)
        ).options(
            selectinload(Post.images),
            selectinload(Post.author),
            selectinload(Post.likes)
        )

        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if user_id not in [user.id for user in session.query(User).join(
                Subscribe,
                Subscribe.author_id == User.id
            ).filter(
                Subscribe.subscriber_id == current_user.id
            ).all()]:
                raise HTTPException(status_code=403,
                                    detail="Not subscribed to this user")
            query = query.filter(Post.author_id == user_id)

        posts = query.all()
        posts_schemas = [
            PostSchema(
                id=post.id,
                images=list(map(lambda x: x.get_filename(), post.images)),
                content=post.content,
                author_id=post.author.id,
                author_name=post.author.fullname,
                created_at=post.created_at,
                count_likes=len(post.likes),
                liked=current_user.id in map(lambda x: x.user_id, post.likes),
                count_comments=len(post.comments),
                is_subscribed=post.author.id in [sub.author_id for sub in
                                                 session.query(
                                                     Subscribe).filter(
                                                     Subscribe.subscriber_id == current_user.id).all()]
            )
            for post in posts
        ]
        return ResponsePostsSchema(posts=posts_schemas)


def get_posts(current_user: CurrentUser,
              user_id: int | None = None) -> ResponsePostsSchema:
    """
        Получает все посты и возвращает их в виде схем.

        Args:
            current_user (CurrentUser): Текущий пользователь.

        Returns:
            ResponsePostsSchema: Схема с информацией о постах.
            :param current_user:
            :param user_id:
        """
    with session_factory() as session:
        # Создание сессии для взаимодействия с базой данных
        query = session.query(Post).options(
            selectinload(Post.images),
            # Загрузка изображений поста
            selectinload(Post.author),
            # Загрузка автора поста
            selectinload(Post.likes))
        if user_id:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            query = query.filter(Post.author_id == user_id)

        posts = query.all()
        posts_schemas = [  # Формирование списка постов в виде схем
            PostSchema(
                id=post.id,
                images=list(
                    map(lambda x: x.get_filename(), post.images)),
                # Список файлов изображений поста
                content=post.content,  # Содержимое поста
                author_id=post.author.id,  # ID автора поста
                author_name=post.author.fullname,  # Имя автора поста
                created_at=post.created_at,  # Дата создания поста
                count_likes=len(post.likes),  # Количество лайков поста
                liked=current_user.id in map(lambda x: x.user_id, post.likes),
                # Проверка, лайкнул ли текущий пользователь этот пост
                count_comments=len(post.comments)
                # Количество комментариев поста
            )
            for post in posts  # Итерирование по всем постам
        ]
        return ResponsePostsSchema(posts=posts_schemas)
        # Возвращение схемы постов в виде ответа


def get_comments(current_user: CurrentUser, post_id: int):
    """
        Получает все комментарии к посту и возвращает их в виде схем.

        Args:
            current_user (CurrentUser): Текущий пользователь.
            post_id (int): Идентификатор поста.

        Returns:
            CommentsOutputSchema: Схема с информацией о комментариях.
        """
    with session_factory() as session:
        # Создание сессии для взаимодействия с базой данных
        comments = session.query(Comment).options(
            selectinload(Comment.user)).filter(
            Comment.post_id == post_id).all()
        # Извлечение всех комментариев к посту из базы данных с загрузкой пользователя
        comments_schemas = [  # Формирование списка комментариев в виде схем
            CommentWithUserSchema(
                id=comment.id,
                user=UserSchema(username=comment.user.username,
                                # Имя пользователя
                                fullname=comment.user.fullname,
                                # Полное имя пользователя
                                birthday=comment.user.birthday,
                                # Дата рождения пользователя
                                signup_at=comment.user.signup_at,
                                # Дата регистрации пользователя
                                last_activity=comment.user.last_activity,
                                # Последняя активность пользователя
                                bio=comment.user.bio,  # Биография пользователя
                                avatar=comment.user.avatar),
                # Аватар пользователя
                post_id=post_id,  # ID поста
                content=comment.content,  # Содержимое комментария
                created_at=comment.created_at,  # Дата создания комментария
                owner=current_user == comment.user,
                # Проверка, является ли текущий пользователь автором комментария
            )
            for comment in comments  # Итерирование по всем комментариям
        ]
        return CommentsOutputSchema(
            comments=comments_schemas)  # Возвращение схемы комментариев в виде ответа


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),  # Вывод в консоль
                        logging.FileHandler('app.log')  # Запись в файл
                    ])

logger = logging.getLogger(__name__)


# async def create_post(current_user: CurrentUser,
#                       content: Annotated[str, Form()],
#                       files: list[UploadFile]) -> None:
#     """
#        Создает новый пост с файлами.
#
#        Args:
#            current_user (CurrentUser): Текущий пользователь.
#            content (str): Содержимое поста.
#            files (list[UploadFile]): Список файлов для загрузки.
#
#        Returns:
#            None
#        """
#     logger.info(f"Создание поста пользователем {current_user.id}")
#
#     with session_factory() as session:
#         # Создается сессия для взаимодействия с базой данных
#         post = Post(content=content, created_at=datetime.now(),
#                     author=current_user)
#         # Создает объект поста с содержимым, текущей датой и автором
#         session.add(post)
#         # Добавляет пост в сессию
#         session.flush()
#         # Сбрасывает изменения, чтобы получить идентификатор поста
#         logger.info(f"Пост создан с ID {post.id}")
#         for file in files:
#             # Итерирует по каждому файлу в списке файлов
#             ext = file.filename.split('.')[-1]
#             # Извлекает расширение файла
#             file_uuid = uuid.uuid4()
#             # Генерирует уникальный идентификатор для файла
#             file_path = settings.PATH_FILES / (str(file_uuid) + "." + ext)
#             # Формирует путь к файлу,
#             # подставляя путь из настроек
#             # с уникальным идентификатором и расширением
#             file_bytes = await file.read()
#             # Асинхронно читает содержимое файла
#             with file_path.open(mode='wb') as f:
#                 f.write(file_bytes)
#                 logger.info(f"Файл сохранен: {file_path}")
#                 # Открывает файл для записи в бинарном режиме
#                 # и записывает содержимое
#             file_model = FileModel(uuid=file_uuid, extension=ext,
#                                    post_id=post.id)
#             # Создает объект FileModel с UUID, расширением
#             # и идентификатором поста
#             session.add(file_model)
#             # Добавляет файл в сессию
#         session.commit()
#         logger.info("Изменения сохранены в базе данных")
#         # Коммитит все изменения в базе данных

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
    logger.info(f"Создание поста пользователем {current_user.id}")

    for file in files:

        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413,
                                detail="Размер файла превышает максимальный предел в 6 МБ.")
        await file.seek(0)

    with session_factory() as session:
        post = Post(content=content, created_at=datetime.now(),
                    author=current_user)
        session.add(post)
        session.flush()
        logger.info(f"Пост создан с ID {post.id}")

        for file in files:
            ext = file.filename.split('.')[-1]
            file_uuid = uuid.uuid4()
            file_path = settings.PATH_FILES / (str(file_uuid) + "." + ext)
            file_bytes = await file.read()
            with file_path.open(mode='wb') as f:
                f.write(file_bytes)
                logger.info(f"Файл сохранен: {file_path}")
            file_model = FileModel(uuid=file_uuid, extension=ext,
                                   post_id=post.id)
            session.add(file_model)

        session.commit()
        logger.info("Изменения сохранены в базе данных")


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
