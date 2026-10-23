"""Question 1b: missing orders.

The API returns pending orders 10 per page. sync_orders should reserve every
order, however many pages there are. There is plenty of stock in each test,
so every order should end up reserved.
"""

from order_sync.fakes import FakeInventoryApi
from order_sync.sync import sync_orders

from tests.helpers import make_orders


def test_one_page_of_orders():
    """5 orders fit on 1 page."""
    api = FakeInventoryApi(orders=make_orders(5), stock={"SKU-1": 100})

    summary = sync_orders(api)

    assert summary["reserved"] == 5, "expected all 5 orders to be reserved"


def test_two_full_pages_of_orders():
    """20 orders fill 2 pages."""
    api = FakeInventoryApi(orders=make_orders(20), stock={"SKU-1": 100})

    summary = sync_orders(api)

    assert summary["reserved"] == 20, "expected all 20 orders to be reserved"


def test_three_pages_with_a_partly_full_last_page():
    """25 orders fill 2 pages, plus 5 orders on a third page."""
    api = FakeInventoryApi(orders=make_orders(25), stock={"SKU-1": 100})

    summary = sync_orders(api)

    assert summary["reserved"] == 25, "expected all 25 orders to be reserved"
