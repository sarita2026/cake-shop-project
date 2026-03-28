from fastapi import APIRouter
from schemas.order_schema import OrderCreate
from services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def place_order(order: OrderCreate):
    order_id = OrderService.create_order(order.dict())
    return {"status": "success", "id": order_id}

@router.get("/")
def get_orders():
    return OrderService.fetch_all()