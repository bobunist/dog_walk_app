from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models.order import OrderModel
from src.serialization.schemas.dog import DogSchema
from src.serialization.schemas.order import OrderRead, OrderWrite
from src.utils.walker_enum import WalkerEnum


class WriteOrderUseCase:
    """Use case for writing an order to the database."""

    async def execute(
        self,
        order: OrderWrite,
        walker: WalkerEnum,
        session: AsyncSession,
    ) -> OrderRead:
        """
        Write an order to the database.

        Args:
            order: Order to write.
            walker: Walker to assign to the order.
            session: Database session.

        Returns:
            OrderRead: Written order.

        """
        order_model = OrderModel(
            walker=walker,
            dog_name=order.dog.name,
            dog_breed=order.dog.breed,
            **order.model_dump(exclude={"dog"}),
        )

        session.add(order_model)
        await session.flush()
        order_read = OrderRead(
            dog=DogSchema(
                name=order_model.dog_name,
                breed=order_model.dog_breed,
            ),
            **order_model.model_dump(exclude={"dog_name", "dog_breed"}),
        )
        return order_read
