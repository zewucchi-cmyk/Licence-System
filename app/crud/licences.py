from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Licence
from core.schemas.licence import LicenceCreate

async def get_all_licences(session: AsyncSession):
    stmt = select(Licence).order_by(Licence.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_licence(session: AsyncSession, licence_create: LicenceCreate):
    licence = Licence(
        key=licence_create.key,
        active=licence_create.active,
        expires_at=datetime.now() + timedelta(days=licence_create.days)
    )

    session.add(licence)
    await session.commit()
    return licence

async def get_licence_by_key(key: str, session: AsyncSession):
    stmt = select(Licence).where(Licence.key == key)
    result = await session.execute(stmt)

    return result.scalars().first()

async def activate_licence(key: str, hwid: str, session: AsyncSession):
    licence = await get_licence_by_key(key=key, session=session)

    if not licence:
        return None

    licence.active = True
    licence.hwid = hwid

    await session.commit()

    return licence

async def verify_licence(key: str, hwid: str, session: AsyncSession):
    licence = await get_licence_by_key(key=key, session=session)

    if licence:
        if licence.active and licence.hwid == hwid and licence.expires_at > datetime.now():
            return True

    return False

