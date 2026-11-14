# Lab 4 — Phân tích kết quả

Đo trên Windows, Flask development server (1 process, threaded) + SQLite file, Locust chạy
cùng máy. Ba kịch bản chạy tuần tự nên DB tích luỹ dần giữa các lần đo.

```powershell
python -m locust -f performance/locustfile.py --headless -H http://127.0.0.1:5000 `
  -u 10 -r 2 -t 30s --html reports/A.html --csv reports/A
python -m locust -f performance/locustfile.py --headless -H http://127.0.0.1:5000 `
  -u 50 -r 5 -t 60s --html reports/B.html --csv reports/B
python -m locust -f performance/locustfile.py --headless -H http://127.0.0.1:5000 `
  -u 200 -r 50 -t 30s --html reports/C.html --csv reports/C
```

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A — baseline | 10 | 2/s | 30s | 19 | 0.00% (0/137) | 4.71 |
| B — load | 50 | 5/s | 60s | 22 | 0.07% (1/1394) | 23.39 |
| C — spike | 200 | 50/s | 30s | 83 | 0.14% (4/2869) | 96.51 |

## 1. Kịch bản nào có p95 cao nhất? Vì sao?

C có p95 cao nhất: **83 ms**, so với 22 ms (B) và 19 ms (A). Trong C, các endpoint
đọc tăng mạnh hơn hẳn: `GET /books` p95 = 87 ms (B: 19 ms), `GET /books/{id}` p95 =
74 ms (B: 17 ms), `POST /books` p95 = 120 ms (B: 31 ms), và p99 tổng = 160 ms,
max = 279 ms (POST).

Nguyên nhân phù hợp với code: 200 user đồng thời dồn request vào Flask development
server một process và SQLite một file. Các request ghi `POST /books` phải chờ nhau
qua SQLite write lock; các request đọc cũng xếp hàng sau đó. RPS tăng gần tuyến tính
theo số user (4.71 → 23.39 → 96.51) nhưng latency tăng phi tuyến (p95 19 → 22 → 83),
tức hệ thống bắt đầu bão hoà chứ chưa "vỡ". Số liệu này chỉ đúng cho môi trường local,
không đại diện cho production.

## 2. Endpoint nào fail rate tăng theo số user?

Các endpoint thật **không có failure**: `GET /books`, `GET /books/{id}`, `POST /books`
đều 0 lỗi ở cả ba kịch bản. `GET /books?year=` tăng 0% (A) → 0.52% (B) → 1.00% (C).
Đây là failure do Locust đánh dấu, **không phải HTTP 500 từ server**: task
`search_by_year()` gọi `response.failure(...)` trên response 200 của mỗi request thứ
100 (đếm bằng `itertools.count`). Vì vậy đúng 1% số lần gọi task này bị tính fail;
tỉ lệ fail tổng bị pha loãng còn 0.07% / 0.14% do task chỉ chiếm weight 1/7.

Response 404 ở `GET /books/{id}` (id ngẫu nhiên không tồn tại) được chủ động đánh dấu
`response.success()` vì đó là hành vi mong đợi, không phải lỗi vận hành.

## 3. SLO p95 < 300 ms — kịch bản nào đạt? Đề xuất CI gate

Cả A, B và C đều đạt p95 < 300 ms trên máy này (19 / 22 / 83 ms). Tuy nhiên đây là
Flask dev server + SQLite, không phải môi trường production, nên không thể kết luận
SLO production từ ba số này.

Đề xuất baseline cho CI:
- **PR smoke (mỗi commit): kịch bản A** — 10 user, 30s. Gate: p95 < 300 ms, failure
  rate < 1%, không có 5xx thật. Chạy nhanh, ít nhiễu.
- **Nightly/regression: kịch bản B** — 50 user, 60s, sát tải dự kiến hơn. Cùng gate
  p95 < 300 ms và failure rate < 1%.
- Không dùng C làm gate trên laptop/CI runner dùng chung; chỉ chạy C trên môi trường
  performance riêng để tránh kết luận sai do CPU/RAM của máy chạy Locust.

## 4. Bonus: connection pool = 5, 200 user đồng thời

Khi pool chỉ có 5 connection, 200 user sẽ tranh nhau connection; request vượt quá
`pool_timeout` sẽ ném timeout (thường thành 500), p95 tăng vọt và failure rate tăng.
Cách xác nhận bằng Locust: cấu hình
`SQLALCHEMY_ENGINE_OPTIONS={"pool_size": 5, "max_overflow": 0, "pool_timeout": 1}`,
chạy lại kịch bản C (thêm `--csv reports/C`), so sánh p95/failure rate với baseline hiện
tại, rồi đọc `reports/C_exceptions.csv` và log server để tìm `TimeoutError` / pool exhaustion.
Nếu muốn thấy rõ hơn, thêm một task giữ connection lâu (slow query) để tăng thời gian
chiếm pool.

## Giới hạn của phép đo

- Flask development server không dùng cho production; WSGI/thread model khác server thật.
- SQLite chỉ có một writer; kết quả bị ảnh hưởng bởi write lock nội bộ.
- Locust và API chạy cùng máy nên tranh CPU/RAM với nhau.
- DB không reset giữa A/B/C nên số bản ghi tăng dần, có thể làm request chậm hơn.
- Có 1% failure được cố ý chèn ở client side để minh hoạ error path, không phải lỗi API.
