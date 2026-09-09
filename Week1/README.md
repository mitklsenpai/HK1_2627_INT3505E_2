# Week 1

## Bài 1: Execute và test

![Kết quả execute và test](../proof_images/Week1/image1.png)

## Bài 2: Health check và echo

### `GET /health`

![Kết quả GET /health](../proof_images/Week1/image2.png)

### `POST /echo`

![Kết quả POST /echo](../proof_images/Week1/image3.png)

## Bài 3: Tạo resource

### `POST` thành công - `201 Created`

![POST 201 Created](../proof_images/Week1/image.png)

### `POST` thiếu name - `400 Bad Request`

![POST 400 thiếu name](../proof_images/Week1/image4.png)

## Bài 4: Path parameters và query string

### Path parameters

#### `GET /books/<book_id>`

![GET book theo book_id](../proof_images/Week1/image5.png)

#### `GET /items/<item_id>`

![GET item theo item_id](../proof_images/Week1/image6.png)

### Query string

Tìm tối đa 5 kết quả có `title = "Python"`.

```python
BOOKS = [
    {"id": "abc-1234", "title": "Python Basic"},
    {"id": "book-001", "title": "Java Programming"},
    {"id": "book-002", "title": "Python Advanced"},
    {"id": "book-003", "title": "C++ Programming"},
    {"id": "book-004", "title": "Python Web Development"},
    {"id": "book-005", "title": "Database"},
]
```

![Kết quả query string](../proof_images/Week1/image%20copy.png)

## Bài 5: Xóa resource

### `DELETE` bị từ chối - `409 Conflict`

![DELETE 409 Cannot delete](../proof_images/Week1/image%20copy%202.png)

### `DELETE` không tìm thấy - `404 Not Found`

![DELETE 404 Not Found](../proof_images/Week1/image%20copy%203.png)

### `DELETE` thành công - `204 No Content`

![DELETE 204 bằng curl](../proof_images/Week1/image%20copy%204.png)

### Log trên server

![Log trên server](../proof_images/Week1/image%20copy%205.png)

## Bài 6: CRUD với books

### `GET /books` - `200 OK`, danh sách books

![GET danh sách books](../proof_images/Week1/image%20copy%206.png)

### `GET /books/<id>` - `200 OK`, chi tiết book tồn tại

![GET chi tiết book tồn tại](../proof_images/Week1/image%20copy%207.png)

### `GET /books/<id>` - `404 Not Found`, book không tồn tại

![GET chi tiết book không tồn tại](../proof_images/Week1/image%20copy%208.png)

### `POST /books` - `201 Created`

![POST tạo book](../proof_images/Week1/image%20copy%209.png)

### `PUT /books/<id>` - `200 OK`

![PUT cập nhật book](../proof_images/Week1/image%20copy%2010.png)

### `DELETE /books/<id>` - `204 No Content`

![DELETE book](../proof_images/Week1/image%20copy%2011.png)

### `POST /books` với body rỗng - `400 Bad Request`

![POST body rỗng](../proof_images/Week1/image%20copy%2012.png)


