from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.models import OrderStatus


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True


class OrderCreateSchema(BaseModel):
    user_id: int
    items: List[OrderItemSchema]


class OrderSchema(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemSchema]

    class Config:
        orm_mode = True
