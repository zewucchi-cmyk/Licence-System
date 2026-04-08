import datetime

from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Licence(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(unique=True, index=True)
    hwid: Mapped[Optional[str]] = mapped_column()
    expires_at: Mapped[datetime.datetime] = mapped_column()
    active: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)