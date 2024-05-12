"""Маршруты для пользователей."""
from fastapi import APIRouter

from users.schemas import UserSchema, Token
from users.services import signup, login_for_access_token

router = APIRouter(prefix="/users", tags=["users"])
router.post("/signup/", response_model=UserSchema)(signup)
router.post("/login/", response_model=Token)(login_for_access_token)
