from datetime import date, time
from secrets import choice

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.order import OrderModel
from src.utils.walker_enum import WalkerEnum


class GetAvailableWorkerUseCase:
    """Use case for getting an available walker."""

    async def execute(
        self,
        walk_date: date,
        walk_time: time,
        session: AsyncSession,
    ) -> WalkerEnum | None:
        """
        Get an available walker for the given date and time.

        Args:
            walk_date: Date to get an available walker for.
            walk_time: Time to get an available walker for.
            session: Database session.

        Returns:
            WalkerEnum | None: Available walker or None if no walker is available.

        """
        query = select(OrderModel.walker).where(
            and_(
                OrderModel.walk_date == walk_date,
                OrderModel.walk_time == walk_time,
            ),
        )
        result = await session.execute(query)
        busy_walkers = result.scalars().all()

        if len(busy_walkers) == 2:
            return None
        if not busy_walkers:
            return choice(list(WalkerEnum))
        if busy_walkers[0] == WalkerEnum.ANTON:
            return WalkerEnum.PETR
        return WalkerEnum.ANTON
