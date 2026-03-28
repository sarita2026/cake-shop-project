from pydantic import BaseModel

class OrderCreate(BaseModel):
    customer_name: str
    phone: str
    address: str
    product: str
    flavor: str
    message: str
    price: float
    payment_type: str

class OrderResponse(OrderCreate):
    id: int
    status: str