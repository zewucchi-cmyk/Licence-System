from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.models.user import User


async def get_user_db(session: AsyncSession = Depends(db_helper.session_getter)):
    yield SQLAlchemyUserDatabase(session, User)