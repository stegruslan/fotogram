"""Схемы pydantic для работы представлений."""
from datetime import datetime

from pydantic import BaseModel


class SignUpSchema(BaseModel):
    """Схема данных для регистрации нового пользователя."""

    username: str
    fullname: str
    password: str
    password_repeat: str
    birthday: datetime | None
    bio: str | None

class UserSchema(BaseModel):
    """Схема данных для возврата информации о пользователе. """

    username: str
    fullname: str
    birthday: datetime | None
    signup_at: datetime
    last_activity: datetime
    bio: str | None
    avatar: str | None

class Token(BaseModel):
    """Токен доступа."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Данные для размещения в токене."""
    username: str | None = None
