import base64
import binascii
import json

from flask import Flask, jsonify, request

from orders_data import ORDERS  # type: ignore[import-not-found]

app = Flask(__name__)

ALLOWED_STATUSES = {"pending", "paid", "shipped", "cancelled"}
ALLOWED_FIELDS = {"id", "customer_id", "status", "price"}
ALLOWED_SORT = {"id", "customer_id", "status", "price"}
DEFAULT_LIMIT = 10
MAX_LIMIT = 50


def _error(status, title, detail=None):
    body = {"error": title, "status": status}
    if detail:
        body["detail"] = detail
    return jsonify(body), status


def _parse_list_param(name):
    values = []
    for raw in request.args.getlist(name):
        for part in raw.split(","):
            part = part.strip()
            if part:
                values.append(part)
    return values


def _parse_limit():
    raw = request.args.get("limit", str(DEFAULT_LIMIT))
    try:
        limit = int(raw)
    except ValueError:
        return None, _error(400, "Invalid limit", f"limit must be an integer, got '{raw}'")
    if not 1 <= limit <= MAX_LIMIT:
        return None, _error(400, "Invalid limit", f"limit must be between 1 and {MAX_LIMIT}")
    return limit, None


def _parse_filters():
    statuses = _parse_list_param("status")
    for s in statuses:
        if s not in ALLOWED_STATUSES:
            return None, None, _error(
                400, "Invalid status",
                f"status must be one of {sorted(ALLOWED_STATUSES)}, got '{s}'",
            )
    raw_cids = _parse_list_param("customer_id")
    customer_ids = []
    for raw in raw_cids:
        try:
            customer_ids.append(int(raw))
        except ValueError:
            return None, None, _error(
                400, "Invalid customer_id", f"customer_id must be an integer, got '{raw}'"
            )
    return statuses, customer_ids, None


def _parse_sort():
    raw = request.args.get("sort", "id").strip() or "id"
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if not parts:
        return None, None, _error(400, "Invalid sort", "sort must not be empty")
    spec = []
    for part in parts:
        desc = part.startswith("-")
        field = part[1:] if desc else part
        if field not in ALLOWED_SORT:
            return None, None, _error(
                400, "Invalid sort field",
                f"sortable fields: {sorted(ALLOWED_SORT)}, got '{part}'",
            )
        spec.append((field, desc))
    # Stable tie-breaker on id
    if not any(f == "id" for f, _ in spec):
        spec.append(("id", False))
    normalized = ",".join(("-" if d else "") + f for f, d in spec)
    return spec, normalized, None


def _parse_fields():
    raw = request.args.get("fields")
    if raw is None or not raw.strip():
        return None, None
    fields = [p.strip() for p in raw.split(",") if p.strip()]
    if not fields:
        return None, _error(400, "Invalid fields", "fields must not be empty")
    for f in fields:
        if f not in ALLOWED_FIELDS:
            return None, _error(
                400, "Invalid fields",
                f"selectable fields: {sorted(ALLOWED_FIELDS)}, got '{f}'",
            )
    fields = list(dict.fromkeys(["id"] + fields))  # id always present
    return fields, None


def _apply_filters(rows, statuses, customer_ids):
    if statuses:
        wanted = set(statuses)
        rows = [o for o in rows if o["status"] in wanted]
    if customer_ids:
        wanted = set(customer_ids)
        rows = [o for o in rows if o["customer_id"] in wanted]
    return rows


def _apply_sort(rows, spec):
    rows = list(rows)
    for field, desc in reversed(spec):  # stable multi-key sort
        rows.sort(key=lambda o: o[field], reverse=desc)
    return rows


def _encode_cursor(last_id, normalized_sort):
    payload = json.dumps({"last_id": last_id, "sort": normalized_sort}).encode()
    return base64.urlsafe_b64encode(payload).decode()


def _decode_cursor(raw):
    try:
        payload = base64.urlsafe_b64decode(raw.encode())
        data = json.loads(payload)
        last_id = int(data["last_id"])
        return {"last_id": last_id, "sort": data.get("sort")}, None
    except (ValueError, KeyError, json.JSONDecodeError, binascii.Error, UnicodeError):
        return None, _error(400, "Invalid cursor", "cursor is malformed or expired")


@app.get("/orders")
def list_orders():
    limit, err = _parse_limit()
    if err:
        return err
    statuses, customer_ids, err = _parse_filters()
    if err:
        return err
    sort_spec, normalized_sort, err = _parse_sort()
    if err:
        return err
    fields, err = _parse_fields()
    if err:
        return err

    rows = _apply_sort(
        _apply_filters(ORDERS, statuses, customer_ids),
        sort_spec,  # type: ignore[arg-type]  # checked via err above, never None here
    )

    start = 0
    cursor_raw = request.args.get("cursor")
    if cursor_raw:
        cursor, err = _decode_cursor(cursor_raw)
        if err:
            return err
        if cursor["sort"] != normalized_sort:  # type: ignore[index]  # checked via err above
            return _error(
                400, "Invalid cursor",
                "cursor was issued for a different sort; keep the same sort or drop cursor",
            )
        idx = next((i for i, o in enumerate(rows) if o["id"] == cursor["last_id"]), None)  # type: ignore[index]  # checked via err above
        if idx is None:
            return _error(400, "Invalid cursor", "cursor does not match any order in scope")
        start = idx + 1

    page = rows[start:start + limit + 1]  # type: ignore[operator]  # checked via err above
    has_more = len(page) > limit  # type: ignore[operator]  # checked via err above
    page = page[:limit]

    next_cursor = _encode_cursor(page[-1]["id"], normalized_sort) if has_more and page else None  # type: ignore[arg-type]  # checked via err above

    if fields is not None:
        data = [{k: o[k] for k in fields} for o in page]
    else:
        data = [dict(o) for o in page]

    links = {}
    if next_cursor:
        args = dict(request.args.to_dict(flat=True))
        args["cursor"] = next_cursor
        qs = "&".join(f"{k}={v}" for k, v in args.items())
        links["next"] = f"/orders?{qs}"

    return jsonify({
        "data": data,
        "meta": {
            "limit": limit,
            "returned": len(data),
            "has_more": has_more,
            "next_cursor": next_cursor,
        },
        "links": links,
    }), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok", "orders": len(ORDERS)}), 200


if __name__ == "__main__":
    app.run(port=5000)
