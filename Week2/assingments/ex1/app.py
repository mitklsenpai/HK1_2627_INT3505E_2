import sqlite3
from flask import Flask, jsonify, request, make_response

def get_db():
    conn = sqlite3.connect("Week2/assingments/ex1/dump_database.bd")
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.get("/orders/<int:oid>")
def get_orders(oid):
    connection = get_db()

    order = connection.execute(
        "select * from books where id = ?",
        (oid,)
    ).fetchone()

    if order is None:
        connection.close()
        return jsonify(error="not found order"), 404

    result = dict(order)
    connection.close()
    return jsonify(result), 200

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)