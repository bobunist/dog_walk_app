import asyncio

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel import SQLModel
from src.config.database import database_config
from src.config.environment import environment_config
from src.utils.mode_enum import ModeEnum


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="module")
async def engine_fixture():
    engine = create_async_engine(database_config.url)
    yield engine
    await engine.dispose()


@pytest.fixture(autouse=True, scope="module")
async def restart_db_fixture(engine_fixture: AsyncEngine) -> None:
    assert environment_config.mode == ModeEnum.TEST.value
    metadata = SQLModel.metadata
    async with engine_fixture.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


@pytest.fixture(
    scope="module",
)
def async_session_maker_fixture(
    engine_fixture: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    session_maker = async_sessionmaker(engine_fixture)
    return session_maker
