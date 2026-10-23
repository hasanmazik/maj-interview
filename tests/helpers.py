from order_sync.fakes import Order


def make_orders(count, sku="SKU-1", qty=1):
    return [Order(f"o-{i}", sku, qty) for i in range(count)]
