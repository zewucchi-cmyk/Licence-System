import datetime

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .product import Product
from .base import Base
from .mixins.int_id_pk import IntIdPKMixin

class Licence(IntIdPKMixin, Base):

    key: Mapped[str] = mapped_column(unique=True, index=True)
    hwid: Mapped[Optional[str]] = mapped_column()
    expires_at: Mapped[datetime.datetime] = mapped_column()
    active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["Product"] = relationship(back_populates="licences")