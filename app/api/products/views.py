from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import User, db_helper
from core.schemas.products import ProductCreate, ProductRead
from core.auth.fastapi_users import current_active_user
from crud import products as products_crud

router = APIRouter(tags=["products"])


@router.post("/create", response_model=ProductRead)
async def create_product(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        product: ProductCreate,
        user: Annotated[User, Depends(current_active_user)]
):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await products_crud.create_product(
        session=session,
        product_create=product,
        author_id=user.id
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
        user: Annotated[User, Depends(current_active_user)]
):
    if not user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return await products_crud.delete_product_by_id(
        session=session,
        product_id=product_id
    )


