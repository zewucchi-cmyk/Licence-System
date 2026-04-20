from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    product_name: str
    key_prefix: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    key_prefix: Optional[str] = None

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int

