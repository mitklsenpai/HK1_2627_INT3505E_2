import sys
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest
from sqlalchemy import event

from product_api import create_app
from product_api.extensions import db
from product_api.models import Order, OrderItem, Product


@pytest.fixture()
def app():
    application = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "LOG_LEVEL": "ERROR",
        }
    )
    with application.app_context():
        db.create_all()
        db.session.add_all(
            [
                Product(sku="SKU-001", name="Keyboard", price_cents=2500, qty_in_stock=5),
                Product(sku="SKU-002", name="Mouse", price_cents=1500, qty_in_stock=0),
            ]
        )
        db.session.commit()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def count_queries(app):
    @contextmanager
    def _counter():
        count = 0

        def _before(*_args):
            nonlocal count
            count += 1

        event.listen(db.engine, "before_cursor_execute", _before)
        try:
            yield lambda: count
        finally:
            event.remove(db.engine, "before_cursor_execute", _before)

    return _counter


def test_create_order_links_products(client):
    resp = client.post(
        "/api/v1/orders",
        json={
            "customer_name": "Nguyen Van A",
            "items": [{"product_id": 1, "qty": 2}, {"product_id": 2, "qty": 1}],
        },
    )
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["customer_name"] == "Nguyen Van A"
    assert {item["product_id"] for item in body["items"]} == {1, 2}
    assert {item["unit_price_cents"] for item in body["items"]} == {2500, 1500}


def test_create_order_merges_duplicate_product_lines(client):
    resp = client.post(
        "/api/v1/orders", json={"items": [{"product_id": 1, "qty": 1}, {"product_id": 1, "qty": 2}]}
    )
    assert resp.status_code == 201
    items = resp.get_json()["items"]
    assert len(items) == 1 and items[0]["qty"] == 3


def test_create_order_unknown_product_returns_404(client):
    resp = client.post(
        "/api/v1/orders", json={"items": [{"product_id": 9999, "qty": 1}]}
    )
    assert resp.status_code == 404


def test_create_order_validation_returns_422(client):
    assert client.post("/api/v1/orders", json={"items": []}).status_code == 422
    assert (
        client.post("/api/v1/orders", json={"items": [{"product_id": 1, "qty": 0}]}).status_code
        == 422
    )


def test_get_order_returns_404(client):
    assert client.get("/api/v1/orders/9999").status_code == 404


def test_get_order_returns_order(client):
    resp = client.post(
        "/api/v1/orders",
        json={"customer_name": "Nguyen Van B", "items": [{"product_id": 1, "qty": 1}]},
    )
    order_id = resp.get_json()["id"]
    resp = client.get(f"/api/v1/orders/{order_id}")
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["id"] == order_id
    assert body["customer_name"] == "Nguyen Van B"
    assert len(body["items"]) == 1
    assert body["items"][0]["product"]["name"] == "Keyboard"


def test_list_orders_uses_eager_loading(client, app, count_queries):
    with app.app_context():
        p = db.session.get(Product, 1)
        for index in range(5):
            order = Order(customer_name=f"customer-{index}")
            order.items.append(OrderItem(product=p, qty=1, unit_price_cents=p.price_cents))
            db.session.add(order)
        db.session.commit()

    with count_queries() as count:
        resp = client.get("/api/v1/orders")

    body = resp.get_json()
    assert resp.status_code == 200
    assert len(body["items"]) == 5
    assert body["items"][0]["items"][0]["product"]["name"] == "Keyboard"
    assert count() == 3


def test_healthz_and_ready(client):
    assert client.get("/healthz").status_code == 200
    assert client.get("/ready").status_code == 200
