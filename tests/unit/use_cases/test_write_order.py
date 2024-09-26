from contextlib import nullcontext
from typing import ContextManager

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.serialization.schemas.order import OrderWrite
from src.use_cases.write_order import WriteOrderUseCase
from src.utils.walker_enum import WalkerEnum


class TestWriteOrder:
    """Test write order use case."""

    @pytest.mark.parametrize(
        "expectation",
        [
            nullcontext(),
            pytest.raises(IntegrityError),
        ],
    )
    async def test_write_order(
        self,
        expectation: ContextManager,
        order_write_fixture: OrderWrite,
        async_session_maker_fixture: async_sessionmaker[AsyncSession],
    ):
        """Test write order use case."""
        with expectation:
            async with async_session_maker_fixture() as session:
                order = await WriteOrderUseCase().execute(
                    order=order_write_fixture,
                    walker=WalkerEnum.PETR,
                    session=session,
                )
                await session.commit()
                assert order
