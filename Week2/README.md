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


## Assignments Ex1: Lấy order theo ID

### `GET /orders/<id>` - Lấy order tồn tại

![GET order theo ID](../proof_images/Week2/assignments/ex1/get%20order.png)

## Assignments Ex3: ETag và cập nhật book

### `GET /books/1` - Lấy book lần đầu và nhận ETag

![Lấy book lần đầu](../proof_images/Week2/assignments/ex3/first%20time%20get%20book.png)

### `GET /books/1` với `If-None-Match` - `304 Not Modified`

![Fetch book với ETag](../proof_images/Week2/assignments/ex3/fetch%20the%20same%20order.png)

### `PATCH /books/1` - Cập nhật book thành công - Đổi lại data mới

![PATCH book](../proof_images/Week2/assignments/ex3/patch%20oder.png)

### `GET /books/1` sau khi cập nhật Etag cập nhật và không trả về 304 nữa

![Lấy book sau khi PATCH](../proof_images/Week2/assignments/ex3/fetch%20after%20patching%20order.png)
