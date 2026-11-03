from flask import Blueprint, jsonify, request
from sqlalchemy.orm import selectinload

from ..errors import NotFound
from ..extensions import db
from ..models import Order, OrderItem, Product
from ..schemas import OrderIn, OrderOut

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")

# Eager load 2 cấp: tránh N+1 khi serialize items và product của từng item.
_ORDER_LOAD = db.select(Order).options(
    selectinload(Order.items).selectinload(OrderItem.product)
)


@orders_bp.get("")
def list_orders():
    rows = db.session.execute(_ORDER_LOAD.order_by(Order.id)).scalars().all()
    return jsonify({"items": [OrderOut().dump(o) for o in rows]}), 200


@orders_bp.get("/<int:id>")
def get_order(id):
    order = db.session.execute(_ORDER_LOAD.where(Order.id == id)).scalar_one_or_none()
    if order is None:
        raise NotFound(message=f"order {id} not found")
    return OrderOut().dump(order), 200


@orders_bp.post("")
def create_order():
    body = OrderIn().load(request.get_json())

    # Gộp các dòng trùng product_id để giữ một OrderItem cho mỗi Product.
    wanted = {}
    for item in body["items"]:
        wanted[item["product_id"]] = wanted.get(item["product_id"], 0) + item["qty"]

    products = (
        db.session.execute(
            db.select(Product).where(
                Product.id.in_(wanted), Product.archived.is_(False)
            )
        )
        .scalars()
        .all()
    )
    by_id = {p.id: p for p in products}
    missing = sorted(set(wanted) - set(by_id))
    if missing:
        raise NotFound(message=f"product {missing[0]} not found")

    order = Order(customer_name=body.get("customer_name") or "guest")
    for product_id, qty in wanted.items():
        product = by_id[product_id]
        order.items.append(
            OrderItem(
                product=product,
                qty=qty,
                unit_price_cents=product.price_cents,
            )
        )
    db.session.add(order)
    db.session.commit()

    saved = db.session.execute(_ORDER_LOAD.where(Order.id == order.id)).scalar_one()
    return OrderOut().dump(saved), 201
