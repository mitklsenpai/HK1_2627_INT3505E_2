from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from ..errors import Conflict, NotFound, OutOfStock
from ..extensions import db
from ..models import Product
from ..schemas import ProductIn, ProductOut, ProductPatch, ReserveIn

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")


def _get_active(product_id):
    product = db.session.get(Product, product_id)
    if product is None or product.archived:
        raise NotFound(message=f"product {product_id} not found")
    return product


def _int_arg(name, default, minimum, maximum):
    raw = request.args.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        from ..errors import BadRequest

        raise BadRequest(message=f"{name} must be an integer")
    return min(maximum, max(minimum, value))


@products_bp.get("")
def list_products():
    page = _int_arg("page", 1, 1, 10_000)
    size = _int_arg("size", 20, 1, 100)

    where = Product.archived.is_(False)
    rows = (
        db.session.execute(
            db.select(Product)
            .where(where)
            .order_by(Product.id)
            .offset((page - 1) * size)
            .limit(size)
        )
        .scalars()
        .all()
    )
    total = db.session.scalar(
        db.select(db.func.count()).select_from(Product).where(where)
    )
    return (
        jsonify(
            {
                "items": [ProductOut().dump(p) for p in rows],
                "page": page,
                "size": size,
                "total": total,
            }
        ),
        200,
    )


@products_bp.get("/<int:id>")
def get_product(id):
    return ProductOut().dump(_get_active(id)), 200


@products_bp.post("")
def create_product():
    body = ProductIn().load(request.get_json())
    product = Product(**body)
    db.session.add(product)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise Conflict(message="sku already exists")
    return ProductOut().dump(product), 201


@products_bp.patch("/<int:id>")
def patch_product(id):
    body = ProductPatch().load(request.get_json(), partial=True)
    product = _get_active(id)
    for key, value in body.items():
        setattr(product, key, value)
    db.session.commit()
    return ProductOut().dump(product), 200


@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    body = ReserveIn().load(request.get_json())
    qty = body["qty"]

    result = db.session.execute(
        db.update(Product)
        .where(
            Product.id == id,
            Product.archived.is_(False),
            Product.qty_in_stock >= qty,
        )
        .values(qty_in_stock=Product.qty_in_stock - qty)
        .execution_options(synchronize_session=False)
    )
    if result.rowcount == 0:
        db.session.rollback()
        product = db.session.get(Product, id)
        if product is None or product.archived:
            raise NotFound(message=f"product {id} not found")
        raise OutOfStock(message=f"only {product.qty_in_stock} left")
    db.session.commit()
    return ProductOut().dump(db.session.get(Product, id)), 200


@products_bp.delete("/<int:id>")
def delete_product(id):
    product = _get_active(id)
    product.archived = True
    db.session.commit()
    return "", 204
