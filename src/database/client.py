from singleton import Singleton
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from src.config.database import database_config


class DatabaseClient(metaclass=Singleton):
    """Client for the database."""

    _async_engine: AsyncEngine | None = None
    _session_maker: async_sessionmaker[AsyncSession] | None = None

    async def get_session(self) -> AsyncSession:
        """Get a session."""
        return self._session_maker()

    async def connect(self) -> None:
        """Connect the client."""
        if self._session_maker is None:
            self._async_engine = create_async_engine(
                database_config.url,
                pool_size=3,
                max_overflow=47,
            )
            self._session_maker = async_sessionmaker(
                self._async_engine,
            )

    async def disconnect(self) -> None:
        """Disconnect the client."""
        if self._async_engine is not None:
            await self._async_engine.dispose()
            self._async_engine = None
            self._session_maker = None
