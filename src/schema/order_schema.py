from pydantic import BaseModel


class OrderRequest(BaseModel):
    size: str
    quantity: int
    pizza_type: str
    toppings: float


class OrderResponse(BaseModel):
    id: int
    size: str
    quantity: int
    price: float
    pizza_type: str
    toppings: float
    order_status: str
    user_id:str

    class Config():
        orm_mode =True

class UpdateOrderStatusRequest(BaseModel):
    new_status: str