# Rà soát bảo mật — API mạng xã hội

Dưới đây là 5 điểm có thể bị lộ hoặc bị khai thác khi triển khai đặc tả OpenAPI của Tuần 6.

| STT | Điểm có thể bị lộ | Hậu quả | Biện pháp cần thực hiện |
|---|---|---|---|
| 1 | `POST /auth/login` cho phép thử mật khẩu không giới hạn hoặc trả lỗi khác nhau giữa email không tồn tại và sai mật khẩu. | Kẻ tấn công dò tài khoản và thử hàng loạt mật khẩu. | Giới hạn tần suất đăng nhập; dùng cùng thông báo `401 invalid_credentials` cho cả hai trường hợp; hạn chế chênh lệch thời gian phản hồi khi có thể. |
| 2 | Mật khẩu được lưu dạng rõ hoặc băm bằng thuật toán quá nhanh như SHA-256. | Khi cơ sở dữ liệu bị lộ, mật khẩu có thể bị đọc hoặc dò nhanh. | Dùng Argon2id hoặc hàm băm mật khẩu phù hợp, với salt riêng cho mỗi mật khẩu và tham số chi phí được điều chỉnh theo hệ thống. |
| 3 | Máy chủ không kiểm tra chữ ký JWT, chấp nhận thuật toán ngoài danh sách cho phép, hoặc bỏ qua thời hạn `exp`. | Token giả mạo hoặc đã hết hạn vẫn có thể đọc bài viết riêng tư. | Cố định thuật toán và khóa ký được phép; kiểm tra chữ ký, `exp` và từ chối token không hợp lệ bằng mã 401. |
| 4 | Refresh token xuất hiện trong log, lưu dạng rõ hoặc vẫn dùng được sau khi đã xoay vòng. | Người có token bị lộ có thể tiếp tục lấy access token mới; token cũ có thể bị phát lại. | Chỉ truyền qua HTTPS; che token trong log; chỉ lưu hash của token; xoay vòng nguyên tử và thu hồi token khi phát hiện dùng lại. |
| 5 | `GET /posts/{id}` chỉ kiểm tra đăng nhập mà bỏ qua scope hoặc quyền sở hữu bài viết. | Người dùng đọc được bài viết riêng tư của người khác (BOLA). | Kiểm tra scope `posts:read` và so khớp `author_id` với người gọi trên mỗi lần đọc; trả 404 cho bài viết không thuộc quyền truy cập. |

Đây là phần rà soát cho **hợp đồng API**, chưa phải kết quả kiểm thử một dịch vụ đang chạy. Các biện pháp trên cần được xác minh thêm bằng mã nguồn và bài kiểm thử khi triển khai backend.
