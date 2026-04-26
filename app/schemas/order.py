from pydantic import BaseModel
from typing import List

class OrderItemRequest(BaseModel):
    product_id: str
    quantity: int


class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItemRequest]


# 👇 ADD THIS
class OrderResponse(BaseModel):
    id: str
    user_id: str
    total_amount: float
    tax_amount: float
    shipping_amount: float
    status: str

    class Config:
        from_attributes = True   # for SQLAlchemy (VERY IMPORTANT)