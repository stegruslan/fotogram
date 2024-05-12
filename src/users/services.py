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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    with (session_factory() as session):
        user = session.query(User).filter_by(username=username).first()
        if not user \
            or not verify_password(password, user.password):
            return
        return user


def create_access_token(data: dict, expires_delta: int = 15):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data.copy(), settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)
    return encoded_jwt


async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=json.dumps({"error": "Could not validate credentials"}),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with session_factory() as session:
        user = session.query(User).filter_by(username=username).first()
        if user is None:
            raise credentials_exception
        return user


def signup(ud: SignUpSchema) -> Response | UserSchema:
    if ud.password != ud.password_repeat:
        return Response(status_code=status.HTTP_400_BAD_REQUEST,
                        content=json.dumps({"error": "Passwords must match"}))
    with session_factory() as session:
        try:
            old_user = session.query(User).filter_by(
                username=ud.username).first()
            if old_user is not None:
                return Response(status_code=status.HTTP_400_BAD_REQUEST,
                                content=json.dumps(
                                    {"error": "Username already taken"}))
            print(old_user)
            user = User(
                username=ud.username,
                fullname=ud.fullname,
                password=get_password_hash(ud.password),
                birthday=ud.birthday,
                bio=ud.bio,
                signup_at=datetime.now(),
                last_activity=datetime.now(),
            )
        except Exception as e:
            return Response(status_code=status.HTTP_400_BAD_REQUEST,
                            content=json.dumps(
                                {"error": "Error creating user"}))
        else:
            session.add(user)
            session.commit()
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
