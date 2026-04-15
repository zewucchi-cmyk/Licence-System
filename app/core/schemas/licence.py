from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

class LicenceBase(BaseModel):
    key: str
    active: bool = False

class LicenceCreate(BaseModel):
    days: int
    product_id: int

class LicenceRead(LicenceBase):
    model_config = ConfigDict(from_attributes=True)

    key: str
    id: int
    expires_at: datetime
    created_at: datetime

