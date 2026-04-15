from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import current_user
from starlette import status

from core.models import User
from core.schemas.licence import LicenceCreate
from core.models.db_helper import db_helper
from core.auth.fastapi_users import current_active_user

from crud import licences as licences_crud

router = APIRouter(tags=["licences"])

@router.post("/")
async def create_licence(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        licence: LicenceCreate,
        user: User = Depends(current_active_user)
):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас недостаточно прав для генерации лицензий")

    return await licences_crud.create_licence(session=session, licence_create=licence)

@router.post("/activate")
async def activate_licence(session: Annotated[AsyncSession, Depends(db_helper.session_getter)], key: str, hwid: str):
    return await licences_crud.activate_licence(session=session, key=key, hwid=hwid)

@router.post("/verify")
async def verify_licence(session: Annotated[AsyncSession, Depends(db_helper.session_getter)], key: str, hwid: str):
    return await licences_crud.verify_licence(session=session, key=key, hwid=hwid)


