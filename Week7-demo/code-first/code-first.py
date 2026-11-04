from flask import Flask, request
from flask_smorest import Api, Blueprint

app = Flask(__name__)
app.config.update(
    API_TITLE="Product API",
    API_VERSION="v1",
    OPENAPI_VERSION="3.0.3",
    OPENAPI_URL_PREFIX="/",
    OPENAPI_SWAGGER_UI_PATH="/swagger-ui",
    OPENAPI_SWAGGER_UI_URL="https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
)

api = Api(app)
blp = Blueprint("Products", __name__, url_prefix="/products")

products = []

@blp.route("/")
def get_products():
    return {"products": products}

@blp.route("/", methods=["POST"])
def add_product():
    product = request.get_json()
    products.append(product)
    return product, 201

api.register_blueprint(blp)

if __name__ == "__main__":
    app.run(debug=True, port = 5000)