import sqlite3
import hashlib
import json
from flask import Flask, jsonify, request, make_response

def get_db():
    conn = sqlite3.connect("Week2/assingments/ex1/dump_database.bd")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.patch("/books/<int:bid>")
def patch(bid):
    if not request.is_json:
        return jsonify(error="expected JSON"), 415

    conn = get_db()

    book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (bid,)
    ).fetchone()

    if book is None:
        conn.close()
        return jsonify(error="not found"), 404

    data = request.get_json(silent=True) or {}

    if "price" in data and data["price"] < 0:
        conn.close()
        return jsonify(error="price must be positive"), 422

    title = data.get("title", book["title"])
    author = data.get("author", book["author"])
    price = data.get("price", book["price"])
    isbn = data.get("isbn", book["isbn"])

    conn.execute("""
        UPDATE books
        SET
            title = ?,
            author = ?,
            price = ?,
            isbn = ?
        WHERE id = ?
    """, (
        title,
        author,
        price,
        isbn,
        bid
    ))

    conn.commit()

    updated_book = conn.execute(
        "SELECT * FROM books WHERE id = ?",
        (bid,)
    ).fetchone()

    conn.close()

    return jsonify(dict(updated_book)), 200

@app.get("/books/<int:bid>")
def get_orders(bid):
    connection = get_db()

    order = connection.execute(
        "select * from books where id = ?",
        (bid,)
    ).fetchone()

    if order is None:
        connection.close()
        return jsonify(error="not found order"), 404

    order = dict(order)

    content = json.dumps(order, sort_keys=True)
    etag = hashlib.md5(content.encode()).hexdigest()

    client_etag = request.headers.get("If-None-Match")

    if client_etag == etag:
        return "", 304

    resp = make_response(jsonify(order))
    resp.headers["ETag"] = etag
    return resp


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)