import datetime
import uuid

import yaml
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

with open("Week4/pet_store/openapi.yaml", encoding="utf-8") as f:
    SPEC = yaml.safe_load(f)


@app.get("/openapi.json")
def spec_json():
    return jsonify(SPEC)


SWAGGER_HTML = """<!doctype html><html><head><meta charset="utf-8"/>
<title>Tasks API - Swagger UI</title>
<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"/></head>
<body><div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>SwaggerUIBundle({url: "/openapi.json", dom_id: "#swagger-ui",
  presets: [SwaggerUIBundle.presets.apis], layout: "BaseLayout"});</script>
</body></html>"""


@app.get("/docs")
def docs():
    return Response(SWAGGER_HTML, content_type="text/html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
