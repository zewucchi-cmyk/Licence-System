from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

class LicenceBase(BaseModel):
    key: str
    active: bool = False

class LicenceCreate(LicenceBase):
    days: int

class LicenceRead(LicenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    expires_at: datetime
    created_at: datetime

