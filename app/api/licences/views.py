from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import User
from core.schemas.licence import LicenceCreate, LicenceUpdate, LicenceExtend
from core.models.db_helper import db_helper
from core.auth.fastapi_users import current_active_user

from crud import licences as licences_crud

router = APIRouter(tags=["licences"])

@router.post("/create")
async def create_licence(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        licence: LicenceCreate,
        user: Annotated[User, Depends(current_active_user)]
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

@router.get("/check-licence")
async def check_licence(session: Annotated[AsyncSession, Depends(db_helper.session_getter)], key: str):
    return await licences_crud.get_licence_by_key(session=session, key=key)

@router.get("/get-all-licences")
async def get_all_licences(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]):
    return await licences_crud.get_all_licences(session=session)

@router.patch("/update-licence")
async def update_licence(session: Annotated[AsyncSession, Depends(db_helper.session_getter)], key: str, update_licence: LicenceUpdate):
    licence = await licences_crud.update_licence(
        session=session,
        key=key,
        update_data=update_licence
    )
    if licence is None:
        raise HTTPException(status_code=404, detail="Licence not found")

    return licence

@router.patch("/extend-licence")
async def extend_licence(session: Annotated[AsyncSession, Depends(db_helper.session_getter)], key:str, extend_data: LicenceExtend, user: Annotated[User, Depends(current_active_user)]):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="abc")

    licence = await licences_crud.extend_licence(
        session=session,
        key=key,
        extend_data=extend_data
    )

    if licence is None:
        raise HTTPException(status_code=404, detail="Licence not found")

    return licence





