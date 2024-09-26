from typing import Annotated

from fastapi import APIRouter, Depends, status
from src.api.controllers.post_order.controller import PostOrderController
from src.api.controllers.post_order.responses import post_order_responses
from src.api.dependencies import SessionDep
from src.serialization.schemas.order import OrderRead, OrderWrite

post_order_router = APIRouter()


@post_order_router.post(
    "/",
    response_model=OrderRead,
    status_code=status.HTTP_201_CREATED,
    summary="Make an order for a dog walk",
    responses=post_order_responses,
)
async def make_order(
    order: OrderWrite,
    session: SessionDep,
    controller: Annotated[PostOrderController, Depends(lambda: PostOrderController())],
) -> OrderRead:
    """
    Make an order for a dog walk.

    Args:
        order: Order to make.
        session: Database session.
        controller: Controller for making an order.

    Returns:
        OrderRead: Made order.

    """
    return await controller.execute(order, session)
