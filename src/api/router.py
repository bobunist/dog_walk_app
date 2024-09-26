from fastapi import APIRouter
from src.api.controllers.get_orders.router import get_orders_router
from src.api.controllers.post_order.router import post_order_router

order_router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

order_router.include_router(post_order_router)
order_router.include_router(get_orders_router)
