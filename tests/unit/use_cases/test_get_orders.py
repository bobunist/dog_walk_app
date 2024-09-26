from datetime import date, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.use_cases.get_orders import GetOrdersUseCase


@pytest.mark.usefixtures("write_petr_order_7_00_fixture")
class TestGetOrders:
    """Test get orders use case."""

    @pytest.mark.parametrize(
        (
            "selected_date",
            "has_orders",
        ),
        [
            (
                datetime.now().date(),
                True,
            ),
            (
                (datetime.now() + timedelta(days=1)).date(),
                False,
            ),
        ],
    )
    async def test_get_orders(
        self,
        selected_date: date,
        has_orders: bool,
        async_session_maker_fixture: async_sessionmaker[AsyncSession],
    ):
        """Test get orders use case."""
        async with async_session_maker_fixture() as session:
            orders = await GetOrdersUseCase().execute(
                selected_date=selected_date,
                session=session,
            )
            assert has_orders == bool(orders)
