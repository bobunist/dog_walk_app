from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status
from src.api.controllers.get_orders.controller import GetOrdersController
from src.api.dependencies import SessionDep
from src.serialization.schemas.order import OrderRead

get_orders_router = APIRouter()


@get_orders_router.get(
    "/",
    response_model=list[OrderRead],
    status_code=status.HTTP_200_OK,
    summary="Get dog walk orders for chosen date.",
)
async def read_orders(
    selected_date: date,
    session: SessionDep,
    controller: Annotated[GetOrdersController, Depends(lambda: GetOrdersController())],
) -> list[OrderRead]:
    """
    Get dog walk orders for chosen date.

    Args:
        selected_date: Date to get orders for.
        session: Database session.
        controller: Controller for getting orders.

    Returns:
        list[OrderRead]: List of orders.

    """
    return await controller.execute(selected_date, session)
