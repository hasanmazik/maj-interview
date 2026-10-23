from order_sync.fakes import Order


def make_orders(count):
    """Return `count` orders named o-0, o-1, o-2, ... Each is for 1 unit of SKU-1."""
    return [Order(id=f"o-{i}", sku="SKU-1", qty=1) for i in range(count)]
