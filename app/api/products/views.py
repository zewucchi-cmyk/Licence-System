from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper
from core.schemas.products import ProductCreate, ProductRead
from core.dependencies.auth import superuser_required
from crud import products as products_crud
from core.constants.errors import (
    PRODUCT_NOT_FOUND
    )

router = APIRouter(tags=["products"])


@router.post("/create", response_model=ProductRead)
async def create_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: ProductCreate,
        admin: Annotated[User, Depends(superuser_required)]
):
    return await products_crud.create_product(
        session=session,
        product_create=product,
        author_id=admin.id
    )


@router.get("/all", response_model=List[ProductRead])
async def get_all_products(session: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> List[ProductRead]:
    return await products_crud.get_all_products(
        session=session
    )


@router.delete("/{product_id}", response_model=ProductRead)
async def delete_product(
        product_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        admin: Annotated[User, Depends(superuser_required)]
):
    product = await products_crud.get_product_by_id(
        session=session,
        product_id=product_id
    )

    if product is None:
        raise HTTPException(status_code=404, detail=PRODUCT_NOT_FOUND % product_id)

    await products_crud.delete_product(
        session=session,
        product=product
    )
    
    return product
