from pydantic import BaseModel
from typing import List
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: float

    class Config:
        orm_mode = True

class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    total: float

    class Config:
        orm_mode = True


class Payment(BaseModel):
    type: str
    amount: float

    class Config:
        orm_mode = True


class ReceiptCreate(BaseModel):
    products: List[ProductCreate]
    payment: Payment


class ReceiptItem(BaseModel):
    id: int
    products: List[Product]
    payment: Payment
    total: float
    rest: float
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class ReceiptItemText(ReceiptItem):
    user_id: int
