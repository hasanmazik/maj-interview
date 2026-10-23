import pytest

from order_sync.fakes import FakeInventoryApi
from order_sync.sync import sync_orders

from tests.helpers import make_orders


@pytest.mark.parametrize("count", [5, 20, 25])
def test_reserves_every_pending_order(count):
    api = FakeInventoryApi(make_orders(count), {"SKU-1": 100})

    summary = sync_orders(api)

    assert summary["reserved"] == count
