from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.order import OrderModel
from src.serialization.schemas.dog import DogSchema
from src.serialization.schemas.order import OrderRead


class GetOrdersUseCase:
    """Use case for getting orders from the database."""

    async def execute(
        self,
        selected_date: date,
        session: AsyncSession,
    ) -> list[OrderRead]:
        """
        Get orders from the database.

        Args:
            selected_date: Date to get orders for.
            session: Database session.

        Returns:
            list[OrderRead]: List of orders.

        """
        query = select(OrderModel).filter_by(walk_date=selected_date)
        result = await session.execute(query)
        order_models = result.scalars().all()
        orders = [
            OrderRead(
                dog=DogSchema(
                    name=order_model.dog_name,
                    breed=order_model.dog_breed,
                ),
                **order_model.model_dump(exclude={"dog_name", "dog_breed"}),
            )
            for order_model in order_models
        ]
        return orders
