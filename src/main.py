from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from src.api.router import order_router
from src.database.client import DatabaseClient


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Lifespan of the application."""
    await DatabaseClient().connect()
    yield
    await DatabaseClient().disconnect()


app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

app.add_middleware(GZipMiddleware)


app.include_router(order_router)
