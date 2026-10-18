# Hướng dẫn tự vẽ ER diagram - Bài 1

Phần này là checklist để hoàn thành ERD cho một trong ba domain mà đề bài cho phép: **thư viện**, **đặt phòng khách sạn**, hoặc **trắc nghiệm online**. Không cần vẽ cả ba domain; chỉ chọn một domain.

## 1. Chọn domain và xác định nghiệp vụ

Viết ngắn gọn 5-8 quy tắc nghiệp vụ trước khi vẽ, ví dụ với domain thư viện:

- Một độc giả có thể mượn nhiều cuốn sách.
- Một cuốn sách có thể có nhiều tác giả.
- Một đầu sách có thể có nhiều bản sao vật lý.
- Mỗi lượt mượn có ngày mượn, hạn trả và ngày trả thực tế.
- Một lượt mượn có thể chứa nhiều bản sao sách.

Các quy tắc này sẽ quyết định entity, thuộc tính và quan hệ trong ERD.

## 2. Bộ entity tối thiểu nên có

Nếu chọn **thư viện**, nên vẽ các entity sau:

- `Reader`: `reader_id` (PK), name, email, phone, created_at.
- `Book`: `book_id` (PK), ISBN, title, publish_year, publisher_id (FK).
- `Author`: `author_id` (PK), name.
- `Publisher`: `publisher_id` (PK), name.
- `Copy`: `copy_id` (PK), book_id (FK), status, shelf_code.
- `Loan`: `loan_id` (PK), reader_id (FK), borrowed_at, due_at, returned_at.
- `LoanItem`: `loan_id` (PK/FK), `copy_id` (PK/FK), fine_amount.
- `BookAuthor`: `book_id` (PK/FK), `author_id` (PK/FK).

`LoanItem` và `BookAuthor` là junction resource/table để biểu diễn quan hệ nhiều-nhiều và chứa metadata.

## 3. Cách nối quan hệ và cardinality

Trên sơ đồ, ghi rõ `1`, `0..1`, `0..N` hoặc `1..N` ở hai đầu quan hệ:

- `Publisher 1 — N Book`.
- `Book 1 — N Copy`.
- `Reader 1 — N Loan`.
- `Loan 1 — N LoanItem`.
- `Copy 1 — N LoanItem` theo lịch sử mượn.
- `Book N — N Author` thông qua `BookAuthor`.

Mọi FK phải trỏ đến đúng PK của entity đích. Nếu quan hệ là N:M, không nối trực tiếp nếu cần lưu thuộc tính của quan hệ; hãy thêm junction entity.

## 4. Quy tắc trình bày ERD

- Dùng ký hiệu Crow's Foot.
- PK gạch chân hoặc đánh dấu `PK`; FK đánh dấu `FK`.
- Tên bảng/entity dùng danh từ số ít, thống nhất kiểu viết.
- Ghi kiểu dữ liệu chính cho từng thuộc tính (`INTEGER`, `VARCHAR`, `DATE`, `DECIMAL`, `BOOLEAN`).
- Đánh dấu thuộc tính bắt buộc/nullable nếu có.
- Tránh thuộc tính lặp như `author1`, `author2`; dùng bảng liên kết.
- Đặt các entity chính ở giữa, junction entity ở giữa hai entity liên quan.

## 5. Kiểm tra trước khi xuất PDF

- Mỗi entity có đúng một PK.
- Mọi FK đều có entity đích và kiểu dữ liệu tương thích.
- Không còn quan hệ N:M chưa được tách.
- Cardinality khớp với các quy tắc nghiệp vụ.
- Tên entity/thuộc tính trong ERD khớp với URL list và JSON Schema.
- Xuất ERD thành PDF, dễ đọc ở mức zoom 100%.

Bạn có thể vẽ bằng draw.io, Lucidchart, dbdiagram.io hoặc công cụ tương đương. Sau khi vẽ xong, dùng chính các entity và quan hệ trong ERD để thiết kế URL list 12-20 endpoint và chọn 3 resource chính để viết JSON Schema.
