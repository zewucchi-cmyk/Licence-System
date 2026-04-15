from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .user import User
    from .licence import Licence

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPKMixin


class Product(IntIdPKMixin,Base):
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    product_name: Mapped[str] = mapped_column()
    key_prefix: Mapped[str] = mapped_column()

    author: Mapped["User"] = relationship(back_populates="products")
    licences: Mapped[List["Licence"]] = relationship(back_populates="product")