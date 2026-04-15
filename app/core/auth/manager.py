import os
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from core.models.user import User
from core.auth.database import get_user_db

SECRET = os.getenv('SECRET')

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"Пользователь {user.username} (ID: {user.id}) Зарегистрировался")

    async def on_after_forgot_password(self, user: User, token:str, request: Optional[Request] = None):
        print(f"Сброс пароля для {user.username} (ID: {user.id}). Токен: {token}")

async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)