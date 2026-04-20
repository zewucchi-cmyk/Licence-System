from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Licence
from core.schemas.licence import LicenceCreate, LicenceUpdate, LicenceExtend
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
        duration_days=licence_create.duration_days,
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

    if licence.is_blocked:
        return False

    licence.active = True
    if licence.expires_at is None:
        licence.expires_at = datetime.now() + timedelta(days=licence.duration_days)
    licence.hwid = hwid

    await session.commit()

    return licence

async def verify_licence(key: str, hwid: str, session: AsyncSession):
    licence = await get_licence_by_key(key=key, session=session)

    if licence is None:
        return False

    if licence.active and licence.hwid == hwid and not licence.is_blocked and licence.expires_at > datetime.now():
        return True

    return False

async def update_licence(key: str, update_data: LicenceUpdate, session: AsyncSession):
    data = update_data.model_dump(exclude_unset=True) if hasattr(update_data, 'model_dump') else update_data
    licence = await get_licence_by_key(key=key, session=session)

    if licence:
        for name, value in data.items():
            setattr(licence, name, value)
        await session.commit()
        await session.refresh(licence)
        return licence
    return None

async def extend_licence(extend_data: LicenceExtend, key: str, session: AsyncSession):
    licence = await get_licence_by_key(key=key, session=session)
    if not licence:
        return None

    total_days = extend_data.days + (extend_data.months * 30)
    delta = timedelta(days=total_days, hours=extend_data.hours)

    now = datetime.now()
    base_date = licence.expires_at if licence.expires_at > now else now

    licence.expires_at = base_date + delta

    await session.commit()
    await session.refresh(licence)
    return licence

