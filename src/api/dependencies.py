from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.client import DatabaseClient

SessionDep = Annotated[
    AsyncSession,
    Depends(DatabaseClient().get_session),
]
