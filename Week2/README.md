# Week 2

## Bài 1: CRUD với books

### `GET /books` - Lấy danh sách books

![GET danh sách books](../proof_images/Week2/get%20books.png)

### `POST /books` - Tạo book thành công

![POST tạo book](../proof_images/Week2/post%20book.png)

### `POST /books` thiếu Content-Type - `415 Unsupported Media Type`

![POST thiếu Content-Type](../proof_images/Week2/content%20type%20missing.png)

### `POST /books` thiếu trường bắt buộc - `422 Unprocessable Entity`

![POST thiếu field](../proof_images/Week2/field%20missing.png)

## Bài 2: Phân trang, lọc và tìm kiếm books

### Phân trang với `page` và `size`

![Phân trang books](../proof_images/Week2/pagination.png)

### Lọc theo tác giả với `author`

![Lọc books theo author](../proof_images/Week2/filter.png)

### Tìm kiếm theo tiêu đề với `q`

![Tìm kiếm books](../proof_images/Week2/search.png)

### Yêu cầu response dạng JSON

![JSON response](../proof_images/Week2/json%20response.png)
