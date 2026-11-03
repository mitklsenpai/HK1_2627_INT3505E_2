import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest

from product_api import create_app
from product_api.extensions import db
from product_api.models import Product


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


def test_list_products_paginates_and_hides_archived(client, app):
    with app.app_context():
        db.session.add(Product(sku="SKU-OLD", name="Old", price_cents=1, archived=True))
        db.session.commit()

    body = client.get("/api/v1/products?page=1&size=1").get_json()

    assert body["page"] == 1 and body["size"] == 1
    assert body["total"] == 2
    assert [p["sku"] for p in body["items"]] == ["SKU-001"]


def test_create_product_returns_201(client):
    resp = client.post(
        "/api/v1/products",
        json={"sku": "SKU-003", "name": "Monitor", "price_cents": 9900},
    )
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["sku"] == "SKU-003"
    assert body["qty_in_stock"] == 0
    assert body["archived"] is False


def test_create_product_rejects_duplicate_sku_with_409(client):
    resp = client.post(
        "/api/v1/products",
        json={"sku": "SKU-001", "name": "Keyboard 2", "price_cents": 100},
    )
    assert resp.status_code == 409
    assert resp.get_json()["error"] == "conflict"


def test_create_product_validation_returns_422(client):
    resp = client.post(
        "/api/v1/products", json={"sku": "x", "name": "Bad", "price_cents": -1}
    )
    assert resp.status_code == 422
    assert resp.get_json()["error"] == "validation_error"
    assert set(resp.get_json()["detail"]) == {"sku", "price_cents"}


def test_get_missing_product_returns_404(client):
    resp = client.get("/api/v1/products/9999")
    assert resp.status_code == 404
    assert resp.get_json()["error"] == "not_found"


def test_reserve_decrements_stock(client):
    resp = client.post("/api/v1/products/1/reserve", json={"qty": 2})
    assert resp.status_code == 200
    assert resp.get_json()["qty_in_stock"] == 3
    assert client.post("/api/v1/products/1/reserve", json={"qty": 4}).status_code == 409


def test_reserve_out_of_stock_returns_409(client):
    resp = client.post("/api/v1/products/2/reserve", json={"qty": 1})
    assert resp.status_code == 409
    assert resp.get_json()["error"] == "out_of_stock"


def test_patch_changes_only_provided_fields(client):
    resp = client.patch("/api/v1/products/1", json={"name": "Keyboard Pro"})
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["name"] == "Keyboard Pro"
    assert body["price_cents"] == 2500


def test_delete_is_soft(client, app):
    assert client.delete("/api/v1/products/1").status_code == 204
    assert client.get("/api/v1/products/1").status_code == 404

    with app.app_context():
        product = db.session.get(Product, 1)
        assert product is not None and product.archived is True
