"""A fake inventory API that runs in memory.

It stands in for a real HTTP service, so the exercise runs without a network.
You do not need to change this file.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    id: str  # for example "o-0"
    sku: str  # the product, for example "SKU-1"
    qty: int  # how many units to reserve


class FakeInventoryApi:
    """An in-memory inventory API with two endpoints.

    list_orders(page)
        Returns one page of pending orders. A page holds up to 10 orders.
        Pages are numbered from 1. The response looks like this:
            {"orders": [Order, ...], "page": 2, "total_pages": 3}

    reserve(order_id, sku, qty)
        Reserves stock for one order and returns an HTTP status code:
            200  reserved
            409  not enough stock
            400  bad request
            503  service unavailable  (temporary)
            429  too many requests    (temporary)

    Tests use `forced_responses` to make reserve() return chosen status codes.
    For example, {"o-0": [503, 503]} makes the first two reserve() calls for
    order o-0 return 503. After that, o-0 is handled normally.

    After a run, tests check these attributes:
        pages_requested  the page numbers passed to list_orders, in order
        attempts         {order id: how many times reserve() was called for it}
        reserved_orders  the ids of the orders that were reserved
    """

    PAGE_SIZE = 10

    def __init__(self, orders, stock, forced_responses=None):
        self._orders = list(orders)
        self.stock = dict(stock)  # {sku: units available}
        self._forced = {order_id: list(codes) for order_id, codes in (forced_responses or {}).items()}

        self.pages_requested = []
        self.attempts = {}
        self.reserved_orders = []

    def list_orders(self, page):
        self.pages_requested.append(page)
        total_pages = math.ceil(len(self._orders) / self.PAGE_SIZE)
        first = (page - 1) * self.PAGE_SIZE
        return {
            "orders": self._orders[first : first + self.PAGE_SIZE],
            "page": page,
            "total_pages": total_pages,
        }

    def reserve(self, order_id, sku, qty):
        self.attempts[order_id] = self.attempts.get(order_id, 0) + 1

        forced = self._forced.get(order_id)
        if forced:
            return forced.pop(0)

        if self.stock.get(sku, 0) < qty:
            return 409
        self.stock[sku] -= qty
        self.reserved_orders.append(order_id)
        return 200
