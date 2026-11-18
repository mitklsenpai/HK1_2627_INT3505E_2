from flask import Flask

from blueprints.v1 import bp as v1_bp
from blueprints.v2 import bp as v2_bp


app = Flask(__name__)
app.json.ensure_ascii = False
app.config["V1_SUNSET"] = "Thu, 31 Dec 2026 23:59:59 GMT"

# register_blueprint overrides, rather than appends to, the blueprint URL prefix.
app.register_blueprint(v1_bp, url_prefix="/api/v1/users")
app.register_blueprint(v2_bp, url_prefix="/api/v2/users")


@app.get("/openapi.json")
def openapi():
    return app.send_static_file("openapi.json")


if __name__ == "__main__":
    app.run(port=5000)
