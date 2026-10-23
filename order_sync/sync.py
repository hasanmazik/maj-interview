"""Reserves stock for every pending order in the inventory API."""


def fetch_all_orders(api):
    """Return every pending order, across all pages."""
    orders = []
    page = 1
    while True:
        result = api.list_orders(page)
        orders.extend(result["orders"])
        page += 1
        if page >= result["total_pages"]:
            break
    return orders


def reserve(api, order):
    """Reserve stock for one order. Returns the HTTP status code."""
    return api.reserve(order.id, order.sku, order.qty)


def sync_orders(api):
    """Reserve stock for every pending order. Returns a count per outcome."""
    summary = {"reserved": 0, "out_of_stock": 0, "failed": 0}
    for order in fetch_all_orders(api):
        status = reserve(api, order)
        if status == 200:
            summary["reserved"] += 1
        elif status == 409:
            summary["out_of_stock"] += 1
        else:
            summary["failed"] += 1
    return summary
