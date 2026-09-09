from flask import Flask, jsonify, request
app = Flask(__name__)

BOOKS = [
    {"id": "abc-1234", "title": "Python Basic"},
    {"id": "book-001", "title": "Java Programming"},
    {"id": "book-002", "title": "Python Advanced"},
    {"id": "book-003", "title": "C++ Programming"},
    {"id": "book-004", "title": "Python Web Development"},
    {"id": "book-005", "title": "Database"},
]


def find_by_id(book_id):
    for book in BOOKS:
        if book["id"] == book_id:
            return book
    return None

# PATH PARAMETER
@app.route("/books/<book_id>", methods=["GET"])
def get_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(book), 200

@app.route("/items/<int:item_id>")
def get_item(item_id = None):
    return jsonify({"id": item_id}), 200

#  QUERY STRING
@app.route("/books", methods=["GET"])
def list_books():
    limit=int(request.args.get("limit", 20))
    q=request.args.get("q","").strip().lower()
    items=[
        b for b in BOOKS 
            if q in b["title"].lower()  
    ]
    items = items[:limit] # Add slice to limit query items, not AI :))
    return jsonify({"items": items}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)