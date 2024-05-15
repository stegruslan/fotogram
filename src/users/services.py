"""Функции для обработки запросов."""
import json
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import status, HTTPException, Depends
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from database import session_factory
from settings import settings
from .models import User
from .schemas import SignUpSchema, UserSchema, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Объект для хэширования паролей.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Объект для аутентификации через OAuth2.


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Принимает два аргумента: пароль в обычном виде и хэшированный пароль.
# Проверяет, соответствует ли хэшированный пароль переданному паролю.
# Возвращает True, если пароли совпадают, и False в противном случае.


def get_password_hash(password):
    return pwd_context.hash(password)


# Принимает пароль в обычном виде.
# Хэширует переданный пароль и возвращает его.

def authenticate_user(username: str, password: str):
    # Принимает имя пользователя и пароль.

    with (session_factory() as session):
        user = session.query(User).filter_by(username=username).first()
        if not user or not verify_password(password, user.password):
            return
        return user
    # Ищем пользователя с указанным именем.
    # Если пользователь не найден или пароль неверен, возвращаем None,
    # Иначе возвращает пользователя.


def create_access_token(data: dict, expires_delta: int = 15):
    # Принимает данные для включения в токен и время его жизни в минутах.
    to_encode = data.copy()
    # Создается копия словаря data, чтобы избежать изменений в исходных данных.
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    # Вычисляем время истечения токена,
    # путем добавления переданного количества минут к текущему времени
    to_encode.update({"exp": expire})
    # Добавляем время истечения с данными,
    # которые будут закодированы в токене.
    encoded_jwt = jwt.encode(data.copy(), settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)
    # Кодируем данные в формат JWT,
    # используя секретный ключ и алгоритм, указанные в настройках
    return encoded_jwt
    # Возвращаем закодированный JWT


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    # Принимает данные формы запроса (имя пользователя и пароль).

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
        data={"sub": user.username},
        # Помещаем имя пользователя в данные токена
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )  # Указываем время жизни токена
    # Возвращаем токен доступа с указанием типа токена
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # Принимает токен доступа
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
    return Response(status_code=200,
                    content=current_user.fullname + " " + current_user.birthday.strftime(
                        "%B %d, %Y"))


def signup(ud: SignUpSchema) -> Response | UserSchema:
    # Принимает данные для регистрации нового пользователя
    # и возвращает либо ответ, либо данные пользователя.
    if ud.password != ud.password_repeat:
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content=json.dumps({"error": "Passwords must match"}))
    # Проверяем, совпадают ли пароли
    with session_factory() as session:
        # Подключаемся к базе данных
        try:
            # Проверяем, существует ли пользователь с таким же именем
            old_user = session.query(User).filter_by(
                username=ud.username).first()
            # Если пользователь уже существует, возвращаем ошибку
            if old_user is not None:
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content=json.dumps(
                                    {"error": "Username already taken"}))
            print(old_user)
            # Создаем нового пользователя с переданными данными
            user = User(
                username=ud.username,
                fullname=ud.fullname,
                password=get_password_hash(ud.password),
                birthday=ud.birthday,
                bio=ud.bio,
                signup_at=datetime.now(),
                last_activity=datetime.now(),
            )
            # Обрабатываем исключение,
            # если произошла ошибка при создании пользователя
        except Exception as e:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content=json.dumps(
                                {"error": "Error creating user"}))
        # Если создание пользователя прошло успешно,
        # добавляем его в базу данных и сохраняем изменения
        else:
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
            # Возвращаем данные пользователя
            return ur
