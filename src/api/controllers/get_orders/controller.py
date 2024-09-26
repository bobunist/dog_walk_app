from datetime import date

from sqlmodel.ext.asyncio.session import AsyncSession
from src.serialization.schemas.order import OrderRead
from src.use_cases.get_orders import GetOrdersUseCase


class GetOrdersController:
    """Controller for getting orders."""

    def __init__(self):
        """Initialize the controller."""
        self._get_orders = GetOrdersUseCase().execute

    async def execute(
        self,
        selected_date: date,
        session: AsyncSession,
    ) -> list[OrderRead]:
        """
        Execute the use case for getting orders.

        Args:
            selected_date: Date to get orders for.
            session: Database session.

        Returns:
            list[OrderRead]: List of orders.

        """
        async with session.begin():
            orders = await self._get_orders(
                selected_date=selected_date,
                session=session,
            )
            return orders
