# Week4 — Tasks API: OpenAPI 3.0.3 + Flask + Swagger UI

## Files

| File | Vai trò |
|---|---|
| `openapi.yaml` | Source of truth: OpenAPI 3.0.3, 1 endpoint `PATCH` |
| `app.py` | Flask implement `PATCH` + `GET /openapi.json` + `GET /docs` |
| `README.md` | File này |

## 2 quyết định thiết kế khó nhất

**1. PATCH thay vì PUT — cập nhật một phần, merge từng field.**
Chỉ giữ một operation `PATCH /v1/tasks/{taskId}` (bài tập chỉ yêu cầu sửa task).
Schema `UpdateTaskInput` khai báo `minProperties: 1` và `additionalProperties: false`
nên app trả 422 khi body rỗng hoặc chứa field không được hỗ trợ (implement trong
`check_task_fields` — `Week4/app.py`); server merge bằng `task.update(...)` nên các
field không gửi lên giữ nguyên giá trị. Chọn PATCH thay vì PUT vì PUT là thay thế
toàn bộ, còn yêu cầu là chỉnh sửa một phần.
*(comment trong spec: `UpdateTaskInput`)*

**2. Auth demo: check sự hiện diện của `Bearer`, không verify JWT thật.**
Spec khai báo `security: bearerAuth` toàn cục nên app phải trả 401 khi thiếu token
(implement trong `require_auth()` — `Week4/app.py`; riêng `/openapi.json` và `/docs`
bỏ qua auth để Swagger UI hoạt động được), nhưng không verify chữ ký để
Try it out chạy được mà không cần IdP. Đánh đổi trung thực: đây là placeholder,
production thay bằng `flask-jwt-extended` hoặc OIDC theo slide Security.
*(comment trong code: `require_auth`)*

## Proof

Test riêng từng phần: Swagger UI render, Try it out, Flask app (`/docs`,
`/openapi.json`) và API bằng curl:

![Swagger UI overview](../proof_images/Week4/swagger_overview.png)
![Try it out PATCH /v1/tasks/{id} → 200](../proof_images/Week4/swagger_try_it_out.png)
![Flask /docs](../proof_images/Week4/flask_docs.png)
![Flask /openapi.json](../proof_images/Week4/openapi_json.png)
![curl PATCH /v1/tasks/{id}](../proof_images/Week4/curl_patch.png)

### Đây là bài tập nhóm, mỗi người chỉ làm một phần, ví dụ với tôi là một endpoint /patch. Sau đó mọi người trong nhóm sẽ họp lại, merge thành một repo chung