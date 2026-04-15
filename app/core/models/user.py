from typing import TYPE_CHECKING, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

if TYPE_CHECKING:
    from .product import Product

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPKMixin



class User(IntIdPKMixin, SQLAlchemyBaseUserTable[int], Base):

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)

    products: Mapped[List["Product"]] = relationship(back_populates="author")