from datetime import datetime

from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict

class LicenceBase(BaseModel):
    key: str
    active: bool = False
    is_blocked: bool = False

class LicenceCreate(BaseModel):
    duration_days: int
    product_id: int

class LicenceUpdate(BaseModel):
    active: Optional[bool] = None
    is_blocked: Optional[bool] = None
    hwid: Optional[str] = None

class LicenceExtend(BaseModel):
    months: int = 0
    days: int = 0
    hours: int = 0

class LicenceRead(LicenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    duration_days: int
    expires_at: Optional[datetime] = None
    created_at: datetime
    hwid: Optional[str] = None
    product_id: int

