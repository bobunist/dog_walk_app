from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from requests import Response


@pytest.mark.parametrize(
    ("selected_date", "orders_expected"),
    [
        ((datetime.now() + timedelta(days=1)).date(), True),
        ((datetime.now() + timedelta(days=2)).date(), False),
    ],
)
def test_get_orders(
    selected_date: datetime.date,
    orders_expected: bool,
    app_client_fixture: TestClient,
    tomorrow_orders_fixture: datetime.date,
):
    response: Response = app_client_fixture.get(
        url="/orders",
        params={
            "selected_date": selected_date,
        },
    )
    orders = response.json()
    assert response.status_code == 200
    assert bool(len(orders)) == orders_expected
