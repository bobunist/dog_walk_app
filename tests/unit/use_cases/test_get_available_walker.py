from datetime import date, datetime, time

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.database.models.order import OrderModel
from src.use_cases.get_available_walker import GetAvailableWorkerUseCase
from src.utils.walker_enum import WalkerEnum


@pytest.mark.asyncio
class TestGetAvailableWalker:
    """Test get available walker use case."""

    async def _write_order_fixture(
        self,
        walk_date: date,
        walk_time: time,
        walker: WalkerEnum,
        session: AsyncSession,
    ) -> None:
        """Write order fixture."""
        fake = Faker()
        order_model = OrderModel(
            flat=str(fake.random_number(3)),
            walker=walker,
            dog_name=fake.name(),
            dog_breed=fake.word(),
            walk_date=walk_date,
            walk_time=walk_time,
        )
        session.add(order_model)
        await session.flush()

    @pytest.mark.parametrize(
        (
            "walk_date",
            "walk_time",
        ),
        [
            (
                datetime.now().date(),
                time(8, 30),
            ),
        ],
    )
    async def test_both_walkers_available(
        self,
        async_session_maker_fixture: async_sessionmaker[AsyncSession],
        walk_date: date,
        walk_time: time,
    ):
        """Test while both walkers available."""
        async with async_session_maker_fixture() as session:
            available_walker = await GetAvailableWorkerUseCase().execute(
                walk_date=walk_date,
                walk_time=walk_time,
                session=session,
            )
            assert available_walker

    @pytest.mark.parametrize(
        (
            "walker",
            "walk_date",
            "walk_time",
        ),
        [
            (
                WalkerEnum.ANTON,
                datetime.now().date(),
                time(7, 00),
            ),
            (
                WalkerEnum.PETR,
                datetime.now().date(),
                time(7, 30),
            ),
        ],
    )
    async def test_one_walker_available(
        self,
        walker: WalkerEnum,
        walk_date: date,
        walk_time: time,
        async_session_maker_fixture: async_sessionmaker[AsyncSession],
    ):
        """Test while one walker available."""
        async with async_session_maker_fixture() as session:
            await self._write_order_fixture(
                walk_date=walk_date,
                walk_time=walk_time,
                walker=walker,
                session=session,
            )
            await session.commit()
        async with async_session_maker_fixture() as session:
            available_walker = await GetAvailableWorkerUseCase().execute(
                walk_date=walk_date,
                walk_time=walk_time,
                session=session,
            )
            assert type(available_walker) is WalkerEnum
            assert available_walker != walker

    @pytest.mark.parametrize(
        (
            "walk_date",
            "walk_time",
        ),
        [
            (
                datetime.now().date(),
                time(8, 30),
            ),
        ],
    )
    async def test_no_walker_available(
        self,
        async_session_maker_fixture: async_sessionmaker[AsyncSession],
        walk_date: date,
        walk_time: time,
    ):
        """Test while no walker available."""
        async with async_session_maker_fixture() as session:
            await self._write_order_fixture(
                walk_date=walk_date,
                walk_time=walk_time,
                walker=WalkerEnum.ANTON,
                session=session,
            )
            await self._write_order_fixture(
                walk_date=walk_date,
                walk_time=walk_time,
                walker=WalkerEnum.PETR,
                session=session,
            )
            await session.commit()
        async with async_session_maker_fixture() as session:
            available_walker = await GetAvailableWorkerUseCase().execute(
                walk_date=walk_date,
                walk_time=walk_time,
                session=session,
            )
            assert available_walker is None
