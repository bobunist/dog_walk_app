from datetime import datetime, time, timedelta

import pytest
from faker import Faker
from fastapi import status
from fastapi.testclient import TestClient
from src.serialization.schemas.dog import DogSchema
from src.serialization.schemas.order import OrderWrite


@pytest.mark.parametrize(
    ("walk_date", "walk_time", "expectations"),
    [
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(7, 30),
            status.HTTP_201_CREATED,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(7, 30),
            status.HTTP_201_CREATED,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(8, 00).isoformat("seconds"),
            status.HTTP_201_CREATED,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(8, 00).isoformat("milliseconds"),
            status.HTTP_201_CREATED,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(8, 30).isoformat("microseconds"),
            status.HTTP_201_CREATED,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(7, 30),
            status.HTTP_409_CONFLICT,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(6, 30),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(23, 30),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            (datetime.now() - timedelta(days=1)).date(),
            time(7, 30),
            status.HTTP_409_CONFLICT,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(7, 31),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            (datetime.now() + timedelta(days=1)).date(),
            time(7, 30, 1),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ],
)
def test_post_order(
    walk_date: datetime.date,
    walk_time: datetime.time,
    expectations: int,
    app_client_fixture: TestClient,
):
    fake = Faker()
    order = OrderWrite.model_construct(
        flat=str(fake.random_number(3)),
        dog=DogSchema(
            breed=fake.word(),
            name=fake.name(),
        ),
        walk_date=walk_date,
        walk_time=walk_time,
    )
    response = app_client_fixture.post(
        "/orders",
        content=order.model_dump_json(),
    )
    assert response.status_code == expectations
