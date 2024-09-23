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
    refresh_token: str

class TokenData(BaseModel):
    """Данные для размещения в токене."""
    username: str | None = None


# class RefreshToken(BaseModel):
#     """Модель refresh token."""
#     token: str
#     expires_at: datetime  # дата и время истечения срока действия токена.


class MessageCreate(BaseModel):
    receiver_id: int
    content: str


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime

    class Config:
        orm_mode = True


class Chat(BaseModel):
    # id: int
    sender_id: int
    receiver_id: int
    content: str


class ChatResponse(BaseModel):
    user_id: int
    user_name: str
    last_message_time: datetime
    last_message_content: str


class UserResponse(BaseModel):
    user_id: int
    fullname: str
    birthday: str
