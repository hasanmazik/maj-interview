import pytest

from order_sync.fakes import FakeInventoryApi
from order_sync.sync import sync_orders

from tests.helpers import make_orders


def test_retries_transient_errors():
    api = FakeInventoryApi(make_orders(1), {"SKU-1": 10}, script={"o-0": [503, 429]})

    summary = sync_orders(api)

    assert api.attempts["o-0"] == 3
    assert summary["reserved"] == 1


def test_gives_up_after_three_attempts():
    api = FakeInventoryApi(make_orders(1), {"SKU-1": 10}, script={"o-0": [503] * 5})

    summary = sync_orders(api)

    assert api.attempts["o-0"] == 3
    assert summary["failed"] == 1


@pytest.mark.parametrize(("status", "outcome"), [(400, "failed"), (409, "out_of_stock")])
def test_does_not_retry_permanent_errors(status, outcome):
    api = FakeInventoryApi(make_orders(1), {"SKU-1": 10}, script={"o-0": [status]})

    summary = sync_orders(api)

    assert api.attempts["o-0"] == 1
    assert summary[outcome] == 1
