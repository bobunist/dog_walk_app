from datetime import datetime, time

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.database.models.order import OrderModel
from src.serialization.schemas.dog import DogSchema
from src.serialization.schemas.order import OrderWrite
from src.utils.walker_enum import WalkerEnum


@pytest.fixture(scope="class")
async def write_petr_order_7_00_fixture(
    async_session_maker_fixture: async_sessionmaker[AsyncSession],
) -> OrderModel:
    async with async_session_maker_fixture() as session:
        fake = Faker()
        order_model = OrderModel(
            flat=str(fake.random_number(3)),
            walker=WalkerEnum.PETR,
            dog_name=fake.name(),
            dog_breed=fake.word(),
            walk_date=datetime.now().date(),
            walk_time=time(7, 0),
        )
        session.add(order_model)
        await session.commit()
        return order_model


@pytest.fixture
def order_write_fixture():
    fake = Faker()
    return OrderWrite(
        flat=str(fake.random_number(3)),
        dog=DogSchema(
            name=fake.name(),
            breed=fake.word(),
        ),
        walk_date=datetime.now().date(),
        walk_time=time(7, 0),
    )
