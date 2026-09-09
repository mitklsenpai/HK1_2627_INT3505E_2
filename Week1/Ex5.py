from flask import Flask, jsonify
ORDERS = {
    "1": {"id": 1, "item": "Laptop", "status": "shipped"},
    "2": {"id": 2, "item": "Phone", "status": "processing"},
    "3": {"id": 3, "item": "Tablet", "status": "delivered"},
    "4": {"id": 4, "item": "Monitor", "status": "pending"}
}

app = Flask(__name__)

@app.route("/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = ORDERS.get(str(order_id))
    if order is None:
        return jsonify({"error": "Not found"}), 404
    if order["status"] in ("shipped", "delivered"):
        return jsonify({"error": "Cannot delete"}), 409
    ORDERS.pop(str(order_id), None)
    return "", 204

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)