from flask import Flask, jsonify, request

app = Flask(__name__)

BOOKS = [
    {"id": 1, "title": "Clean Code", "author": "R. Martin", "year": 2008},
    {
        "id": 2,
        "title": "The Pragmatic Programmer",
        "author": "David Thomas",
        "year": 1999,
    },
]

_next = 3


def find_book(book_id):
    return next((book for book in BOOKS if book["id"] == book_id), None)


@app.route("/books", methods=["GET"])
def list_books():
    books = BOOKS.copy()

    # Search: /books?q=python
    query = request.args.get("q")

    if query:
        query = query.lower()
        books = [
            book
            for book in books
            if query in book["title"].lower()
            or query in book["author"].lower()
        ]

    # Sort: /books?sort=title
    sort = request.args.get("sort")

    if sort == "title":
        books.sort(key=lambda book: book["title"].lower())

    return jsonify(books), 200


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)

    if not book:
        return jsonify({"error": "not found"}), 404

    return jsonify(book), 200


@app.route("/books", methods=["POST"])
def create_book():
    global _next

    body = request.get_json(silent=True) or {}

    title = body.get("title")
    author = body.get("author")
    year = body.get("year")

    if not title or not author or year is None:
        return jsonify({"error": "title, author and year are required"}), 400

    if not isinstance(year, int):
        return jsonify({"error": "year must be an integer"}), 400

    if year < 1900:
        return jsonify({"error": "year must be >= 1900"}), 400

    book = {
        "id": _next,
        "title": title,
        "author": author,
        "year": year,
    }

    _next += 1
    BOOKS.append(book)

    return jsonify(book), 201, {"Location": f"/books/{book['id']}"}


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = find_book(book_id)

    if not book:
        return jsonify({"error": "not found"}), 404

    body = request.get_json(silent=True) or {}

    if "year" in body:
        if not isinstance(body["year"], int):
            return jsonify({"error": "year must be an integer"}), 400

        if body["year"] < 1900:
            return jsonify({"error": "year must be >= 1900"}), 400

    book.update(body)

    return jsonify(book), 200


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)

    if not book:
        return jsonify({"error": "not found"}), 404

    BOOKS.remove(book)

    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)


