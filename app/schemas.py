from typing import Optional
from pydantic import BaseModel, Field
import datetime


class Product(BaseModel):
    id: int
    name: str
    sku: str
    price: float
    quantity: int
    category: str
    created_at: datetime.datetime


class ProductCreate(BaseModel):
    name: str
    sku: str
    price: float
    quantity: int
    category: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, gt=0)
    category: Optional[str] = None