from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Licence
from core.schemas.licence import LicenceCreate
from core.utils.keygen import generate_licence_key
from crud.products import get_product_by_id

async def get_all_licences(session: AsyncSession):
    stmt = select(Licence).order_by(Licence.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_licence(session: AsyncSession, licence_create: LicenceCreate):
    product = await get_product_by_id(session=session, product_id=licence_create.product_id)

    if not product:
        return None

    key = generate_licence_key(product.key_prefix)

    licence = Licence(
        key=key,
        active=licence_create.active,
        expires_at=datetime.now() + timedelta(days=licence_create.days),
        product_id=licence_create.product_id,
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

