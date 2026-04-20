from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product
from core.schemas.products import ProductCreate

async def get_all_products(session: AsyncSession):
    stmt = select(Product).order_by(Product.id)
    result = await session.scalars(stmt)
    return result.all()

async def get_product_by_id(session: AsyncSession, product_id: int):
    return await session.get(Product, product_id)

async def create_product(session: AsyncSession, product_create: ProductCreate, author_id: int):
    product = Product(
        author_id=author_id,
        product_name=product_create.product_name,
        key_prefix=product_create.key_prefix,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

async def update_product(session: AsyncSession, product_id: int, update_data: dict):
    data = update_data.model_dump(exclude_unset=True) if hasattr(update_data, "model_dump") else update_data
    product = await get_product_by_id(session, product_id)
    if product:
        for name, value in data.items():
            setattr(product, name, value)
        await session.commit()
        await session.refresh(product)
        return product
    return None

async def delete_product_by_id(session: AsyncSession, product_id: int):
    product = await get_product_by_id(session, product_id)
    if product:
        await session.delete(product)
        await session.commit()
        return True
    return False
