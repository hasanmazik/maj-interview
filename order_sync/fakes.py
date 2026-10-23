"""A local stand-in for the inventory HTTP API.

You do not need to edit this file. It lets the exercise run offline with no
accounts, containers or network.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    id: str
    sku: str
    qty: int


class FakeInventoryApi:
    """Behaves like a small inventory HTTP API.

    `script` forces responses for an order before normal handling, e.g.
    {"o-1": [503, 503]} answers 503 twice for o-1, then behaves normally.
    """

    PAGE_SIZE = 10

    def __init__(self, orders, stock, script=None):
        self._orders = list(orders)
        self.stock = dict(stock)
        self._script = {order_id: list(statuses) for order_id, statuses in (script or {}).items()}

        # What the tests inspect.
        self.pages_requested = []
        self.attempts = {}  # order id -> reserve calls received for it
        self.reservations = []  # order ids reserved successfully

    def list_orders(self, page):
        """GET /orders?page=N. Returns one page of pending orders.

        {"orders": [Order, ...], "page": N, "total_pages": T}
        """
        self.pages_requested.append(page)
        total_pages = math.ceil(len(self._orders) / self.PAGE_SIZE)
        start = (page - 1) * self.PAGE_SIZE
        return {
            "orders": self._orders[start : start + self.PAGE_SIZE],
            "page": page,
            "total_pages": total_pages,
        }

    def reserve(self, order_id, sku, qty):
        """POST /reservations. Returns an HTTP status code.

        200 reserved, 409 not enough stock. 503 (unavailable) and 429 (too many
        requests) can also happen.
        """
        self.attempts[order_id] = self.attempts.get(order_id, 0) + 1
        scripted = self._script.get(order_id)
        if scripted:
            return scripted.pop(0)
        if self.stock.get(sku, 0) < qty:
            return 409
        self.stock[sku] -= qty
        self.reservations.append(order_id)
        return 200
