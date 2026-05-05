from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.licence import LicenceCreate, LicenceUpdate, LicenceExtend, LicenceRead
from core.models.db_helper import db_helper

from crud import licences as licences_crud
from core.dependencies.auth import superuser_required
from core.constants.errors import (
    LICENCE_NOT_FOUND,
    CANNOT_FREEZE,
    CANNOT_ACTIVATE,
    HWID_MISMATCH,
    CANNOT_UNFREEZE
)

router = APIRouter(tags=["licences"])


# ADMIN ENDPOINTS (Superuser required)

@router.post("/create", response_model=LicenceRead, status_code=status.HTTP_201_CREATED)
async def create_licence(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        licence: LicenceCreate,
        admin: Annotated[User, Depends(superuser_required)]
):
    return await licences_crud.create_licence(session=session, licence_create=licence)


@router.get("/get-all-licences", response_model=Sequence[LicenceRead])
async def get_all_licences(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        admin: Annotated[User, Depends(superuser_required)]
):
    return await licences_crud.get_all_licences(session=session)


@router.patch("/{key}/update-licence", response_model=LicenceRead)
async def update_licence(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        key: str,
        update_licence: LicenceUpdate,
        admin: Annotated[User, Depends(superuser_required)]
):
    licence = await licences_crud.update_licence(
        session=session,
        key=key,
        update_data=update_licence
    )
    if licence is None:
        raise HTTPException(status_code=404, detail=LICENCE_NOT_FOUND % key)
    return licence


@router.patch("/{key}/extend-licence", response_model=LicenceRead)
async def extend_licence(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        key: str,
        extend_data: LicenceExtend,
        admin: Annotated[User, Depends(superuser_required)]
):
    licence = await licences_crud.extend_licence(
        session=session,
        key=key,
        extend_data=extend_data
    )
    if licence is None:
        raise HTTPException(status_code=404, detail=LICENCE_NOT_FOUND % key)
    return licence


# USER/SYSTEM ENDPOINTS

@router.post("/{key}/verify", response_model=LicenceRead)
async def verify_licence(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    key: str,
    hwid: str
):
    result = await licences_crud.verify_licence(session=session, key=key, hwid=hwid)

    if result is None:
        raise HTTPException(status_code=404, detail=LICENCE_NOT_FOUND % key)

    if result == "not_activated":
        result = await licences_crud.activate_licence(
            session=session,
            key=key,
            hwid=hwid
        )

        if result is False:
             raise HTTPException(status_code=400, detail=CANNOT_ACTIVATE % key)

    if result == "hwid_mismatch":
        raise HTTPException(status_code=403, detail=HWID_MISMATCH % key)

    if result is False:
        raise HTTPException(status_code=403, detail="Licence is blocked or expired")

    return result


@router.get("/{key}/check-licence", response_model=LicenceRead)
async def check_licence(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        key: str
):
    licence = await licences_crud.get_licence_by_key(session=session, key=key)
    if licence is None:
        raise HTTPException(status_code=404, detail=LICENCE_NOT_FOUND % key)
    return licence


@router.patch("/{key}/freeze", response_model=LicenceRead)
async def freeze_licence(
        key: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    result = await licences_crud.freeze_licence(key=key, session=session)
    if result is None:
        raise HTTPException(status_code=404, detail=LICENCE_NOT_FOUND % key)
    if result is False:
        raise HTTPException(status_code=400, detail=CANNOT_FREEZE % key)
    return result


@router.patch("/{key}/unfreeze", response_model=LicenceRead)
async def unfreeze_licence(
        key: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    result = await licences_crud.unfreeze_licence(key=key, session=session)
    if result is None:
        raise HTTPException(status_code=404, detail=LICENCE_NOT_FOUND % key)
    if result is False:
        raise HTTPException(status_code=400, detail=CANNOT_UNFREEZE % key)
    return result
