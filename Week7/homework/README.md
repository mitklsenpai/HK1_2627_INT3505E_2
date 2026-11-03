# Week 7 — Homework: Orders và Health Check

## 1. Tạo đơn hàng

![POST tạo đơn hàng có hai sản phẩm trả HTTP 201](../../proof_images/Week7/homework/03_order_create.png)

## 2. Danh sách đơn hàng

![GET danh sách đơn hàng cùng các dòng hàng và sản phẩm](../../proof_images/Week7/homework/01_list_orders.png)

## 3. Chi tiết đơn hàng

![GET chi tiết đơn hàng số 1 trả HTTP 200](../../proof_images/Week7/homework/02_order_get.png)

## 4. Sản phẩm không tồn tại

![POST đơn hàng tham chiếu sản phẩm không tồn tại trả HTTP 404](../../proof_images/Week7/homework/04_unknown_product_404.png)

## 5. Gộp các dòng trùng sản phẩm

![Hai dòng cùng sản phẩm được gộp thành một dòng số lượng 3](../../proof_images/Week7/homework/06_merge_duplicate_items.png)

## 6. Kiểm tra dữ liệu đơn hàng

![Đơn hàng rỗng bị từ chối với HTTP 422](../../proof_images/Week7/homework/08_order_validation_422.png)

## 7. Liveness và readiness

![Healthz và ready đều trả HTTP 200, kết nối database hoạt động](../../proof_images/Week7/homework/05_healthz_ready.png)

## 8. Kiểm thử tự động

![Kết quả pytest Homework với 17 kiểm thử thành công](../../proof_images/Week7/homework/07_pytest.png)
