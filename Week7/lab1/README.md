# Week 7 — Lab1: Product API

## 1. Danh sách sản phẩm và phân trang

![GET danh sách sản phẩm với page=1, size=1 và total=2](../../proof_images/Week7/lab1/01_list_products.png)

## 2. Chi tiết sản phẩm

![GET sản phẩm 1 trả về Keyboard](../../proof_images/Week7/lab1/02_get_product.png)

## 3. Tạo sản phẩm

![POST tạo Monitor trả HTTP 201](../../proof_images/Week7/lab1/03_create_product.png)

## 4. Từ chối SKU trùng

![POST trùng SKU trả HTTP 409 conflict](../../proof_images/Week7/lab1/04_duplicate_sku_409.png)

## 5. Cập nhật một phần

![GET trước và PATCH sau cho thấy chỉ tên sản phẩm thay đổi](../../proof_images/Week7/lab1/05_patch_product.png)

## 6. Giữ hàng và giảm tồn kho

![Reserve 2 sản phẩm làm tồn kho giảm từ 5 xuống 3](../../proof_images/Week7/lab1/06_reserve.png)

## 7. Từ chối khi không đủ hàng

![Reserve vượt tồn kho trả 409 và không làm thay đổi số lượng](../../proof_images/Week7/lab1/07_out_of_stock_409.png)

## 8. Xóa mềm

![DELETE 204, GET 404 và bản ghi SQLite có archived bằng 1](../../proof_images/Week7/lab1/08_soft_delete.png)

## 9. Kiểm tra dữ liệu đầu vào

![POST dữ liệu không hợp lệ trả 422 và chi tiết lỗi từng trường](../../proof_images/Week7/lab1/09_validation_422.png)

## 10. Kiểm thử tự động

![Kết quả pytest Lab1 với 9 kiểm thử thành công](../../proof_images/Week7/lab1/12_pytest.png)

## 11. Migration cơ sở dữ liệu

![Alembic upgrade thành công và SQLite có revision cùng bảng products](../../proof_images/Week7/lab1/13_migration.png)
