import datetime
import uuid

import yaml
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

with open("Week4/openapi.yaml", encoding="utf-8") as f:
    SPEC = yaml.safe_load(f)


TASKS = {
    "3fa85f64-5717-4562-b3fc-2c963f66afa6":
        {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6", "title": "Họp nhóm API team",
         "status": "open", "priority": "high", "dueDate": "2026-09-15"},
    "9b7ec0ec-6eb5-4d62-8b6a-111111111111":
        {"id": "9b7ec0ec-6eb5-4d62-8b6a-111111111111", "title": "Viết openapi.yaml",
         "status": "done", "priority": "normal"},
}

STATUSES = {"open", "done"}
PRIORITIES = {"low", "normal", "high"}
FIELDS = {"title", "status", "priority", "dueDate", "assigneeId"}


def problem(status, title, detail, instance):
    """Lỗi theo RFC 7807 application/problem+json (khớp components.schemas.Error)."""
    body = {"type": f"https://api.example.vn/errors/{title.lower().replace(' ', '-')}",
            "title": title, "status": status, "detail": detail, "instance": instance}
    return Response(__import__("json").dumps(body), status=status,
                    content_type="application/problem+json")


def require_auth():
    """Demo auth: chỉ cần header Authorization: Bearer <gì cũng được>.
    Không verify JWT thật để Try it out chạy được; thiếu header -> 401 đúng spec."""
    if request.headers.get("Authorization", "").startswith("Bearer ") is False:
        return problem(401, "Unauthorized", "thiếu header Authorization: Bearer <token>",
                       request.path)


def find_task(task_id):
    """Chuẩn hoá taskId về UUID; id sai dạng hoặc không tồn tại -> None (404)."""
    try:
        normalized = str(uuid.UUID(task_id))
    except ValueError:
        return None
    return TASKS.get(normalized)


def check_task_fields(data):
    """Validate body PATCH: chặn field lạ (additionalProperties: false), check enum, date."""
    if not isinstance(data, dict):
        return "body phải là JSON object"
    unknown = set(data) - FIELDS
    if unknown:
        return f"field không được hỗ trợ: {', '.join(sorted(unknown))}"
    if "title" in data and not str(data["title"]).strip():
        return "title minLength 1"
    if "status" in data and data["status"] not in STATUSES:
        return "status phải là open|done"
    if "priority" in data and data["priority"] not in PRIORITIES:
        return "priority phải là low|normal|high"
    if "dueDate" in data and data["dueDate"] is not None:
        try:
            datetime.date.fromisoformat(data["dueDate"])
        except (TypeError, ValueError):
            return "dueDate phải RFC 3339 date (VD 2026-09-15)"
    if not data:
        return "PATCH cần ít nhất 1 field (minProperties 1)"
    return None


@app.patch("/v1/tasks/<taskId>")
def patch_task(taskId):
    if (e := require_auth()) is not None:
        return e
    task = find_task(taskId)
    if task is None:
        return problem(404, "Task not found", f"task {taskId} không tồn tại", request.path)
    data = request.get_json(silent=True)
    if data is None:
        return problem(400, "Bad Request", "body phải là JSON hợp lệ", request.path)
    if (err := check_task_fields(data)) is not None:
        return problem(422, "Validation Error", err, request.path)
    if "title" in data:
        data["title"] = data["title"].strip()
    task.update(data)
    return jsonify(task)


@app.get("/openapi.json")
def spec_json():
    """Trả spec machine-readable, sinh trực tiếp từ openapi.yaml (không copy tay)."""
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
    """Swagger UI trỏ về /openapi.json (doc sinh từ spec, không sửa tay)."""
    return Response(SWAGGER_HTML, content_type="text/html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)