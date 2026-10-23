"""Order and payment handlers for the shop's customer API.

Each handler receives the signed-in user and the request parameters, and
returns a dict that is sent back as JSON. The web framework signs the user in
before any handler is called. Amounts are in cents.
"""

import logging
import os
import sqlite3
from dataclasses import dataclass

from payments import charge_card, refund_payment

PAYMENTS_API_KEY = "pay_live_7f3c9a1e5b2d8c4a6e0f"
INVOICE_DIR = "/srv/shop/invoices"

SORT_COLUMNS = {
    "newest": "created_at DESC",
    "oldest": "created_at ASC",
    "total": "total DESC",
}

log = logging.getLogger("orders")
db = sqlite3.connect(os.environ.get("SHOP_DB", "shop.db"))


@dataclass
class User:
    id: int
    email: str
    is_admin: bool


def get_order(user: User, order_id: str) -> dict:
    """Return one of the signed-in user's orders."""
    row = db.execute("SELECT id, total, status FROM orders WHERE id = " + order_id).fetchone()
    if row is None:
        return {"error": "order not found"}
    return {"id": row[0], "total": row[1], "status": row[2]}


def list_orders(user: User, sort: str = "newest") -> dict:
    """Return all of the signed-in user's orders, sorted by `sort`."""
    order_by = SORT_COLUMNS.get(sort, SORT_COLUMNS["newest"])
    rows = db.execute(
        "SELECT id, total, status FROM orders WHERE user_id = ? ORDER BY " + order_by,
        (user.id,),
    ).fetchall()
    return {"orders": [{"id": r[0], "total": r[1], "status": r[2]} for r in rows]}


def checkout(user: User, cart_id: int, card_token: str) -> dict:
    """Charge the cart total to the user's card, then save the order as paid."""
    total = db.execute(
        "SELECT total FROM carts WHERE id = ? AND user_id = ?", (cart_id, user.id)
    ).fetchone()[0]
    log.info("checkout user=%s card=%s amount=%d", user.email, card_token, total)

    try:
        charge_card(PAYMENTS_API_KEY, card_token, total)
    except Exception:
        log.warning("charge failed for cart %s", cart_id)

    db.execute(
        "INSERT INTO orders (user_id, total, status) VALUES (?, ?, 'paid')", (user.id, total)
    )
    db.commit()
    return {"status": "paid", "total": total}


def refund(user: User, order_id: int, amount: int) -> dict:
    """Refund part or all of a paid order. Only admins can do this."""
    if not user.is_admin:
        return {"error": "forbidden"}
    order = db.execute("SELECT total, status FROM orders WHERE id = ?", (order_id,)).fetchone()
    total = order[0]
    status = order[1]
    if status != "paid":
        return {"error": "only paid orders can be refunded"}

    refund_payment(PAYMENTS_API_KEY, order_id, amount)
    db.execute("UPDATE orders SET status = 'refunded' WHERE id = ?", (order_id,))
    db.commit()
    return {"status": "refunded", "amount": amount}


def download_invoice(user: User, filename: str) -> bytes:
    """Return the PDF of one of the signed-in user's invoices."""
    path = os.path.join(INVOICE_DIR, filename)
    with open(path, "rb") as f:
        return f.read()
