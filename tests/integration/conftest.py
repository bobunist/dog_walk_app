from datetime import datetime, time, timedelta

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.database.models.order import OrderModel
from src.main import app
from src.utils.walker_enum import WalkerEnum


@pytest.fixture
def app_client_fixture() -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
async def tomorrow_orders_fixture(
    async_session_maker_fixture: async_sessionmaker[AsyncSession],
) -> datetime.date:
    fake = Faker()
    tomorrow_datetime = datetime.now() + timedelta(days=1)
    async with async_session_maker_fixture() as session:
        orders = [
            OrderModel(
                flat=str(fake.random_number(3)),
                walker=WalkerEnum.PETR.value if i % 2 else WalkerEnum.ANTON.value,
                dog_name=fake.name(),
                dog_breed=fake.word(),
                walk_date=tomorrow_datetime.date(),
                walk_time=time(hour=7 + (i // 2), minute=(i % 2) * 30),
            )
            for i in range(10)
        ]
        session.add_all(orders)
        await session.flush()
        await session.commit()
        return tomorrow_datetime.date()
