"""Функции для обработки запросов."""
import json
from datetime import datetime, timedelta, timezone
from typing import Annotated, List
from fastapi import status, HTTPException, Depends, WebSocket, \
    WebSocketDisconnect
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import Body
from database import session_factory
from settings import settings
from . import models, schemas
from .models import User, Subscribe, Message, ChatMessage
from .schemas import SignUpSchema, UserSchema, Token, ChatResponse, \
    UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Объект для хэширования паролей.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Объект для аутентификации через OAuth2.


def verify_password(plain_password, hashed_password):
    """
        Проверяет соответствие хэшированного пароля переданному паролю.

        Args:
            plain_password (str): Пароль в обычном виде.
            hashed_password (str): Хэшированный пароль.

        Returns:
            bool: True, если пароли совпадают, иначе False.
        """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
        Хэширует переданный пароль.

        Args:
            password (str): Пароль в обычном виде.

        Returns:
            str: Хэшированный пароль.
        """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    """
        Аутентифицирует пользователя по имени пользователя и паролю.

        Args:
            username (str): Имя пользователя.
            password (str): Пароль в обычном виде.

        Returns:
            User | None: Пользователь, если аутентификация прошла успешно,
            иначе None.
        """

    with (session_factory() as session):
        user = session.query(User).filter_by(username=username).first()
        if not user or not verify_password(password, user.password):
            return
        return user
    # Ищем пользователя с указанным именем.
    # Если пользователь не найден или пароль неверен, возвращаем None,
    # Иначе возвращает пользователя.


def create_access_token(data: dict, expires_delta: int = 15):
    """
        Создает JWT токен доступа.

        Args:
            data (dict): Данные для включения в токен.
            expires_delta (int, optional): Время жизни токена в минутах.
            Defaults to 15.

        Returns:
            str: Закодированный JWT токен.
        """
    # Принимает данные для включения в токен и время его жизни в минутах.
    to_encode = data.copy()
    # Создается копия словаря data, чтобы избежать изменений в исходных данных.
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    # Вычисляем время истечения токена,
    # путем добавления переданного количества минут к текущему времени
    to_encode.update({"exp": expire,
                      "user_id": data["user_id"]})
    # Добавляем время истечения с данными,
    # которые будут закодированы в токене.
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)
    # Кодируем данные в формат JWT,
    # используя секретный ключ и алгоритм, указанные в настройках
    return encoded_jwt
    # Возвращаем закодированный JWT


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
        Обрабатывает запрос на получение токена доступа.

        Args:
            form_data (OAuth2PasswordRequestForm): Данные формы запроса
            (имя пользователя и пароль).

        Returns:
            Token: Токен доступа и тип токена.
        """

    # Аутентифицируем пользователя,
    # используя переданные имя пользователя и пароль
    user = authenticate_user(form_data.username, form_data.password)

    # Если пользователь не аутентифицирован
    # (не найден или неверный пароль), вызываем HTTP исключение
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаем токен доступа для аутентифицированного пользователя
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        # Помещаем имя пользователя в данные токена
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )  # Указываем время жизни токена
    # Возвращаем токен доступа с указанием типа токена
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
        Получает текущего пользователя по токену доступа.

        Args:
            token (str): Токен доступа.

        Returns:
            User: Текущий пользователь.
        """

    # Создание HTTP исключения для случая,
    # когда учетные данные не могут быть проверены
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=json.dumps({"error": "Could not validate credentials"}),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Декодируем токен, используя секретный ключ и алгоритм,
        # указанные в настройках
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        exp: int = payload.get("exp")
        token_date = datetime.fromtimestamp(exp, timezone.utc)
        if token_date.replace(tzinfo=timezone.utc) < datetime.now(
            timezone.utc):
            raise credentials_exception
        # Получаем имя пользователя из данных токена
        username: str = payload.get("sub")
        # Если имя пользователя отсутствует в данных токена,
        # вызываем исключение
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # Подключаемся к базе данных
    # и ищем пользователя с указанным именем пользователя
    with session_factory() as session:
        user = session.query(User).filter_by(username=username).first()
        # Если пользователь не найден, вызываем исключение
        if user is None:
            raise credentials_exception
        # Возвращаем найденного пользователя
        return user


CurrentUser = Annotated[User, Depends(get_current_user)]


# Принимает аргумент current_user,
# который представляет собой текущего пользователя,
# аннотированного как CurrentUser
# Автоматически извлечет текущего пользователя,
# используя зависимость get_current_user
async def read_users_me(
    current_user: CurrentUser,
):
    """
        Возвращает информацию о текущем пользователе.

        Args:
            current_user (User): Текущий пользователь.

        Returns:
            Response: Ответ с информацией о пользователе.
        """
    user_data = UserResponse(
        user_id=current_user.id,
        fullname=current_user.fullname,
        birthday=current_user.birthday.strftime("%B %d, %Y")
    )
    return JSONResponse(content=user_data.dict())


def signup(ud: SignUpSchema):
    """
    Регистрирует нового пользователя.

    Args:
        ud (SignUpSchema): Данные для регистрации.

    Returns:
        UserSchema: Данные зарегистрированного пользователя.
    """

    if ud.password != ud.password_repeat:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Passwords must match")

    try:
        with session_factory() as session:
            # Проверяем, существует ли пользователь с таким же именем
            if session.query(User).filter_by(
                username=ud.username).first() is not None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Username already taken")

            # Создаем нового пользователя
            user = User(
                username=ud.username,
                fullname=ud.fullname,
                password=get_password_hash(ud.password),
                birthday=ud.birthday,
                bio=ud.bio,
                signup_at=datetime.now(),
                last_activity=datetime.now(),
            )

            session.add(user)
            session.commit()

            # Формируем объект данных пользователя для возврата
            ur = UserSchema(
                id=user.id,
                username=user.username,
                fullname=user.fullname,
                signup_at=user.signup_at,
                bio=user.bio,
                last_activity=user.last_activity,
                avatar=user.avatar,
                birthday=user.birthday,
            )
            return ur

    except SQLAlchemyError as e:
        # Ловим ошибки SQLAlchemy и возвращаем более детализированное сообщение
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Error creating user")
    except Exception as e:
        # Ловим любые другие исключения
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Unexpected error occurred")


def subscribe(current_user: CurrentUser, author_id: int) -> Response:
    """
        Подписывает текущего пользователя на автора.

        Args:
            current_user (User): Текущий пользователь.
            author_id (int): ID автора.

        Returns:
            Response: Ответ с результатом операции.
        """
    # Создаем сессию для работы с базой данных.
    with session_factory() as session:
        # Ищем автора по ID.
        author = session.query(User).filter_by(id=author_id).first()
        # Если автор не найден, выбрасываем HTTP исключение с кодом 404.
        if author is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Author not found")
        # Ищем запись о подписке текущего пользователя на этого автора.
        current_subscribe = session.query(Subscribe).filter(
            and_(Subscribe.subscriber == current_user,
                 Subscribe.author == author)).first()
        # Если подписки нет, создаем новую запись о подписке.
        if not current_subscribe:
            current_subscribe = Subscribe(author=author,
                                          subscriber=current_user)
            # Добавляем новую запись в сессию.
            session.add(current_subscribe)
            # Сохраняем изменения в базе данных.
            session.commit()
        # Возвращаем ответ с кодом 200 (OK).
        return Response(status_code=status.HTTP_200_OK)


def unsubscribe(current_user: CurrentUser, author_id: int) -> Response:
    """
        Отписывает текущего пользователя от автора.

        Args:
            current_user (User): Текущий пользователь.
            author_id (int): ID автора.

        Returns:
            Response: Ответ с результатом операции.
        """
    # Создаем сессию для работы с базой данных.
    with session_factory() as session:
        # Ищем автора по ID.
        author = session.query(User).filter_by(id=author_id).first()
        # Если автор не найден, выбрасываем HTTP исключение с кодом 404.
        if author is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Author not found")
        # Ищем запись о подписке текущего пользователя на этого автора.
        current_subscribe = session.query(Subscribe).filter(
            Subscribe.author == author).filter(
            Subscribe.subscriber == current_user).first()
        # Если подписка существует, удаляем ее.
        if current_subscribe:
            session.delete(current_subscribe)
            # Сохраняем изменения в базе данных.
            session.commit()
        # Возвращаем ответ с кодом 200 (OK).
        return Response(status_code=status.HTTP_200_OK)


def send_message(
    message: schemas.MessageCreate,
    current_user: models.User = Depends(get_current_user)
):
    with session_factory() as session:
        sender = session.query(User).filter_by(id=current_user.id).first()
        if sender is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Author not found")
        db_message = models.Message(
            sender_id=current_user.id,
            receiver_id=message.receiver_id,
            content=message.content,
        )
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
        return db_message


def get_messages(
    current_user: models.User = Depends(get_current_user)
):
    with session_factory() as session:
        messages = session.query(models.Message).filter(
            (models.Message.sender_id == current_user.id) |
            (models.Message.receiver_id == current_user.id)
        ).order_by(models.Message.timestamp).all()
        return messages




def open_get_send_chat(
    chat: schemas.Chat,
    current_user: models.User = Depends(get_current_user)
):
    with session_factory() as session:
        # Получаем историю сообщений между текущим пользователем и указанным получателем
        history_messages = session.query(models.Message).filter(
            (models.Message.sender_id == current_user.id) &
            (models.Message.receiver_id == chat.receiver_id) |
            (models.Message.sender_id == chat.receiver_id) &
            (models.Message.receiver_id == current_user.id)
        ).order_by(models.Message.timestamp).all()

        # Если история сообщений пустая и есть содержимое для отправки, отправляем новое сообщение
        if not history_messages and chat.content:
            new_message = models.Message(
                sender_id=current_user.id,
                receiver_id=chat.receiver_id,
                content=chat.content,
                timestamp=datetime.now()
                # Устанавливаем текущее время как временную метку сообщения
            )
            session.add(new_message)
            session.commit()
            session.refresh(new_message)
            # Обновляем историю сообщений, добавляя только что отправленное сообщение
            history_messages = [new_message]

        # Возвращаем историю сообщений
        return history_messages


def get_user_name(user_id: int) -> str:
    with session_factory() as session:
        user = session.query(models.User).filter(
            models.User.id == user_id).one_or_none()
        if user:
            return schemas.UserSchema(
                username=user.username,
                fullname=user.fullname,
                birthday=user.birthday,
                signup_at=user.signup_at,
                last_activity=user.last_activity,
                bio=user.bio,
                avatar=user.avatar
            )
        else:
            raise HTTPException(status_code=404, detail="User not found")


def get_all_chats(
    current_user: models.User = Depends(get_current_user)
):
    with session_factory() as session:
        # Получаем все сообщения, отправленные и полученные текущим пользователем
        chats_query = session.query(
            models.Message.receiver_id,
            models.Message.sender_id,
            models.Message.content.label('last_message_content'),
            models.Message.timestamp.label('last_message_time')
        ).filter(
            (models.Message.sender_id == current_user.id) |
            (models.Message.receiver_id == current_user.id)
        ).order_by(models.Message.timestamp.desc())

        # Группируем сообщения по чату
        chats = {}
        for message in chats_query.all():
            # Определяем идентификатор чата
            chat_id = (message.sender_id, message.receiver_id) \
                if message.sender_id != current_user.id \
                else (message.receiver_id, message.sender_id)

            # Сохраняем последнее сообщение для данного чата
            if chat_id not in chats:
                chats[chat_id] = {
                    'receiver_id': chat_id[1] if chat_id[
                                                     0] == current_user.id else
                    chat_id[0],
                    'content': message.last_message_content,
                    'timestamp': message.last_message_time
                }

        # Преобразуем чаты в список объектов сообщений
        chat_list = [
            models.Message(
                sender_id=current_user.id,
                receiver_id=chat['receiver_id'],
                content=chat['content'],
                timestamp=chat['timestamp']
            )
            for chat in chats.values()
        ]

        return chat_list
