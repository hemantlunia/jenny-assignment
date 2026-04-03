from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load data from file
with open("customers.json") as f:
    customers = json.load(f)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/customers")
def get_customers():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))

        start = (page - 1) * limit
        end = start + limit

        data = customers[start:end]

        return jsonify({
            "data": data,
            "total": len(customers),
            "page": page,
            "limit": limit
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/customers/<int:customer_id>")
def get_customer(customer_id):
    for c in customers:
        if c["customer_id"] == customer_id:
            return jsonify(c)
    return jsonify({"error": "Customer not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)