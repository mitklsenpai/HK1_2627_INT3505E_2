# Review Public API: Google AI Studio (Gemini API)
## Thông tin 
- Public API: Google Studio AI (Gemini): 
"https://generativelanguage.googleapis.com/v1beta/models/{model-name}"
- Họ và tên: Nguyễn Trần Quang Tuyển
- Là thành viên của nhóm 6
- Nhiệm vụ: Đánh giá tiêu chí 8 (Authentication & Scurity) + tiêu chí 9 (Versioning & Deprecation) - Chit tiết xem ở bên dưới

## 1. Authentication & Security

### 1.1 Authentication — API Key bắt buộc

```http
POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent
x-goog-api-key: AIzaSy...ĐÚNG
Content-Type: application/json

{
  "contents": [{ "parts": [{ "text": "Hello" }] }]
}
```

```http
HTTP/1.1 200 OK

{
  "candidates": [{ "content": { "parts": [{ "text": "..." }] } }]
}
```

### 1.2 Security

- Key truyền ở **Header** (`x-goog-api-key`), không lộ qua URL.
- Key sai / không tồn tại → `400`.
```bash
export GOOGLE_API_KEY="AIzaSy..."
```

#### Rate limit

| Loại | Ý nghĩa | Minh họa |
| --- | --- | --- |
| RPM | Requests / minute | Quá 50 requests → `429` |
| TPM | Tokens / minute | Vượt quota token → `429` |
| RPD | Requests / day | Hết quota ngày → `429` |


Ví dụ: Rate limit khi gửi quá 50 requests/phút
```http
HTTP/1.1 429 Too Many Requests

{
  "error": {
    "code": 429,
    "message": "Quota exceeded",
    "status": "RESOURCE_EXHAUSTED"
  }
}
```

## 2. Versioning & Deprecation

### 2.1 Versioning

Version rõ ràng trong path:

```text
/v1beta/models/gemini-3.8-flash:generateContent
/v1/models/
```

| Version | Vai trò |
| --- | --- |
| `/v1beta` | Thử nghiệm tính năng mới |
| `/v1` | Ổn định cho production |

### 2.2 Deprecation

Google duy trì lộ trình rõ ràng qua docs: model nào dừng, thời gian dừng, model thay thế, thông báo cho user.

| Trạng thái | Ví dụ |
| --- | --- |
| Đang hoạt động | Model hiện tại, được hỗ trợ đầy đủ |
| Ngừng hỗ trợ | Model cũ → migrate sang model khác theo docs |

## 4. Minh họa Request / Response

<details>
<summary>REQUEST với API Key đúng → RESPONSE 200</summary>

```bash
curl -H "x-goog-api-key: $GOOGLE_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"contents":[{"parts":[{"text":"Hi"}]}]}' \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
```

→ `200` + nội dung model trả về.

</details>

<details>
<summary>REQUEST với API không tồn tại → RESPONSE 400</summary>

```bash
curl -H "x-goog-api-key: KEY_SAI" \
     "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
```

→ `400 API key not valid`.

</details>

<details>
<summary>Quá 50 requests → 429</summary>

```bash
for i in {1..50}; do
  echo "Request $i"

  curl -s -o /tmp/response.json -w "HTTP: %{http_code}\n" \
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
      "contents": [
        {
          "parts": [
            {
              "text": "Hello"
            }
          ]
        }
      ]
    }'

  cat /tmp/response.json
done
```
</details>
