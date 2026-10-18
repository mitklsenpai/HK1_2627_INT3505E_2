from jsonschema import validate, ValidationError
from flask import Blueprint, request, jsonify
from sqlalchemy import and_, or_
from models import db, Book, Category
import json
import base64
from pathlib import Path

SCHEMA = json.loads((Path(__file__).resolve().parents[1] / "schemas" / "book.json").read_text(encoding="utf-8"))

books_bp = Blueprint("books", __name__)

DEFAULT_LIMIT = 20
MAX_LIMIT = 100
SORT_FIELDS = {
    "id": Book.id,
    "title": Book.title,
    "price_vnd": Book.price_vnd,
    "stock": Book.stock,
}


def _parse_limit():
    raw = request.args.get("limit", DEFAULT_LIMIT, type=int)
    if raw is None or raw < 1:
        return None, (jsonify(error="invalid_limit", message="limit must be >= 1"), 400)
    return min(raw, MAX_LIMIT), None


def _parse_sort(raw):
    keys = []
    for token in (raw or "-id").split(","):
        token = token.strip()
        descending = token.startswith("-")
        name = token[1:] if descending else token
        if not name or name not in SORT_FIELDS:
            return None, (jsonify(error="invalid_sort", message=f"unsupported sort field: {name}"), 400)
        keys.append((name, SORT_FIELDS[name], descending))
    if not any(name == "id" for name, _, _ in keys):
        keys.append(("id", Book.id, False))
    return keys, None


def _encode_cursor(sort, values):
    payload = json.dumps({"sort": sort, "values": values}, separators=(",", ":"))
    return base64.urlsafe_b64encode(payload.encode()).decode().rstrip("=")


def _decode_cursor(raw):
    try:
        padding = "=" * (-len(raw) % 4)
        return json.loads(base64.urlsafe_b64decode((raw + padding).encode()).decode())
    except (ValueError, TypeError, json.JSONDecodeError):
        return None


def _cursor_filter(sort_keys, values):
    branches = []
    for index, (_, column, descending) in enumerate(sort_keys):
        equal_prefix = [sort_keys[j][1] == values[j] for j in range(index)]
        operator = column < values[index] if descending else column > values[index]
        branches.append(and_(*equal_prefix, operator))
    return or_(*branches)


@books_bp.route("/api/v1/books", methods=["GET"])
def list_books():
    limit, error = _parse_limit()
    if error:
        return error
    assert limit is not None  # narrow cho type checker; nhánh lỗi đã return ở trên

    sort_raw = request.args.get("sort", "-id")
    sort_keys, error = _parse_sort(sort_raw)
    if error:
        return error
    assert sort_keys is not None

    strategy = request.args.get("strategy", "cursor").lower()
    if strategy not in {"cursor", "offset"}:
        return jsonify(error="invalid_strategy", message="strategy must be offset or cursor"), 400

    query = db.select(Book).join(Category, isouter=True)
    genre = request.args.get("genre")
    if genre:
        query = query.where(or_(Category.slug == genre, Category.name == genre))

    order_by = [column.desc() if descending else column.asc() for _, column, descending in sort_keys]
    query = query.order_by(*order_by)

    if strategy == "offset":
        offset = request.args.get("offset", 0, type=int)
        if offset is None or offset < 0:
            return jsonify(error="invalid_offset", message="offset must be >= 0"), 400
        rows = db.session.scalars(query.offset(offset).limit(limit + 1)).all()
        more = len(rows) > limit
        data = rows[:limit]
        next_offset = offset + limit if more else None
        return jsonify(data=[book.to_dict() for book in data], page={"strategy": "offset", "offset": offset, "limit": limit, "more": more, "next_offset": next_offset})

    raw_cursor = request.args.get("cursor")
    if raw_cursor:
        cursor = _decode_cursor(raw_cursor)
        if not cursor or cursor.get("sort") != sort_raw or len(cursor.get("values", [])) != len(sort_keys):
            return jsonify(error="invalid_cursor", message="cursor is invalid or does not match sort"), 400
        query = query.where(_cursor_filter(sort_keys, cursor["values"]))

    rows = db.session.scalars(query.limit(limit + 1)).all()
    more = len(rows) > limit
    data = rows[:limit]
    next_cursor = None
    if more and data:
        values = [getattr(data[-1], name) for name, _, _ in sort_keys]
        next_cursor = _encode_cursor(sort_raw, values)
    return jsonify(data=[book.to_dict() for book in data], page={"strategy": "cursor", "limit": limit, "more": more, "next": next_cursor})

@books_bp.route("/api/v1/books", methods=["POST"])
def create_book():
    payload = request.get_json(silent=True)
    try:
        validate(payload, SCHEMA) # input schema riêng
    except ValidationError as e:
        return jsonify({
            "error": "validation_failed",
            "field": list(e.path),
            "message": e.message
        }), 400
    book = Book.from_payload(payload) # cần cài đặt
    db.session.add(book); 
    db.session.commit()
    return book.to_dict(), 201
