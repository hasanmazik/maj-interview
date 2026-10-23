"""Question 1a: retries.

The API sometimes answers with a temporary error: 503 or 429. sync_orders
should try again, up to 3 attempts in total. It should not retry answers that
will not change, such as 400 (bad request) or 409 (not enough stock).
"""

from order_sync.fakes import FakeInventoryApi
from order_sync.sync import sync_orders

from tests.helpers import make_orders


def test_retries_temporary_errors_until_it_succeeds():
    """The first call returns 503, the second 429, and the third succeeds."""
    api = FakeInventoryApi(
        orders=make_orders(1),
        stock={"SKU-1": 10},
        forced_responses={"o-0": [503, 429]},
    )

    summary = sync_orders(api)

    assert api.attempts["o-0"] == 3, "expected 2 failed attempts, then 1 that succeeds"
    assert summary["reserved"] == 1


def test_stops_after_three_attempts():
    """Every call returns 503, so the order fails after 3 attempts."""
    api = FakeInventoryApi(
        orders=make_orders(1),
        stock={"SKU-1": 10},
        forced_responses={"o-0": [503, 503, 503, 503, 503]},
    )

    summary = sync_orders(api)

    assert api.attempts["o-0"] == 3, "expected exactly 3 attempts, then give up"
    assert summary["failed"] == 1


def test_does_not_retry_a_bad_request():
    """400 means the request itself is wrong. Sending it again will not help."""
    api = FakeInventoryApi(
        orders=make_orders(1),
        stock={"SKU-1": 10},
        forced_responses={"o-0": [400]},
    )

    summary = sync_orders(api)

    assert api.attempts["o-0"] == 1, "a 400 should not be retried"
    assert summary["failed"] == 1


def test_does_not_retry_when_out_of_stock():
    """There is no stock, so the API answers 409. Sending it again will not help."""
    api = FakeInventoryApi(
        orders=make_orders(1),
        stock={"SKU-1": 0},
    )

    summary = sync_orders(api)

    assert api.attempts["o-0"] == 1, "a 409 should not be retried"
    assert summary["out_of_stock"] == 1
