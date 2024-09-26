from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession
from src.api.exceptions.date_time_passed import DatetimePassedException
from src.api.exceptions.time_is_busy import TimeIsBusyException
from src.serialization.schemas.order import OrderRead, OrderWrite
from src.use_cases.get_available_walker import GetAvailableWorkerUseCase
from src.use_cases.write_order import WriteOrderUseCase


class PostOrderController:
    """Controller for making an order."""

    def __init__(self):
        """Initialize the controller."""
        self._get_available_walker = GetAvailableWorkerUseCase().execute
        self._write_order = WriteOrderUseCase().execute

    async def execute(
        self,
        order: OrderWrite,
        session: AsyncSession,
    ) -> OrderRead:
        """
        Execute the use case for making an order.

        Args:
            order: Order to make.
            session: Database session.

        Returns:
            OrderRead: Made order.

        """
        async with session.begin():
            current_datetime = datetime.now()
            if (
                current_datetime.date()
                > datetime.combine(
                    date=order.walk_date,
                    time=order.walk_time,
                ).date()
            ):
                raise DatetimePassedException()

            available_walker = await self._get_available_walker(
                walk_date=order.walk_date,
                walk_time=order.walk_time,
                session=session,
            )

            if available_walker is None:
                raise TimeIsBusyException()

            new_order = await self._write_order(
                order=order,
                walker=available_walker,
                session=session,
            )
            return new_order
