# Đồ án: P2P Range Queries via Prefix Hash Trees (PHT)

**Thông tin sinh viên thực hiện:**

- **Sinh viên:** Trần Lê Quang Hữu
- **Nhóm:** N23dccn024
- **Học phần:** Cơ sở dữ liệu phân tán

---

## 1. Tổng quan dự án

Dự án triển khai thuật toán **Prefix Hash Tree (PHT)** trên nền tảng mạng **Distributed Hash Table (DHT)** để tối ưu hóa bài toán truy vấn khoảng (Range Queries) trong hệ cơ sở dữ liệu phân tán ngang hàng (P2P).

Thông thường, Standard DHTs gặp hạn chế lớn khi xử lý truy vấn khoảng do tính chất băm ngẫu nhiên phá vỡ tính địa phương của dữ liệu. Dự án này khắc phục điều đó bằng cách sử dụng PHT để tổ chức không gian dữ liệu linh hoạt, giúp giảm thiểu tối đa chi phí thông điệp (Message Overhead).

## 2. Các tính năng chính

- **Dynamic Space Partitioning:** Tự động phân chia không gian dữ liệu và chẻ nhánh (split node) khi tập dữ liệu tại một điểm vượt ngưỡng lưu trữ an toàn.
- **Pruning Mechanism:** Cơ chế cắt tỉa thông minh giúp thuật toán chủ động loại bỏ các nhánh không liên quan để tối ưu hóa thời gian tìm kiếm.
- **Churn Resilience (Chịu lỗi):** Tự động bẻ lái (Rerouting) truy vấn sang các Node dự phòng (Replica) khi phát hiện sự cố sập máy chủ vật lý, đảm bảo không rò rỉ dữ liệu.
- **Topology Visualization:** Tích hợp thư viện NetworkX để trực quan hóa cấu trúc đồ thị mạng lưới và đường đi thực tế của truy vấn.

## 3. Cây thư mục

````text
CSDL_PT_FINAL/
├── __pycache__/                     # Thư mục cache tự động sinh của Python
├── .venv/                           # Môi trường ảo Python (Virtual Environment)
├── dataset/
│   └── iot_telemetry_data.csv       # Dữ liệu thời tiết thực tế lấy từ Open-Meteo API
├── dht.py                           # Cốt lõi của Distributed Hash Table (Logic định tuyến SHA-256)
├── fetch_data.py                    # Script kết nối API và tải dữ liệu môi trường
├── peer.py                          # Định nghĩa cấu trúc và hoạt động của từng máy chủ ngang hàng
├── pht.py                           # Thuật toán Prefix Hash Tree & Pruning Logic
├── query.py                         # Module xử lý các loại truy vấn (Point Lookup, Range Query)
├── README.md                        # Tài liệu hướng dẫn (File này)
├── requirements.txt                 # Danh sách các thư viện phụ thuộc của dự án
├── scenario_failover.py             # Kịch bản 1: Mô phỏng sự cố "Kill Node" và phục hồi
├── scenario_normal.py               # Kịch bản 2: Benchmark Range Query vs Standard DHT
└── visualization.py                 # Module đồ họa, vẽ sơ đồ cấu trúc cây và mạng lưới
## 4. Hướng dẫn chạy dự án

Yêu cầu máy tính đã cài đặt **Python 3.8** trở lên. Bạn hãy mở Terminal (hoặc Command Prompt) tại thư mục chứa code và chạy lần lượt các lệnh sau:

**Bước 1: Cài đặt các thư viện cần thiết**

```bash
pip install pandas networkx matplotlib requests
````

**Bước 2: Tải dữ liệu thời tiết thực tế**
Lệnh này sẽ tự động tải dữ liệu của Hà Nội và lưu vào thư mục dataset.

```bash
python fetch_data.py
```

**Bước 3: Chạy kịch bản thuật toán bình thường**
Lệnh này sẽ chạy truy vấn tìm dải nhiệt độ 20°C - 30°C, so sánh hiệu năng và vẽ đồ thị mạng lưới.

```bash
python scenario_normal.py
```

**Bước 4: Chạy kịch bản giả lập sập máy chủ (Failover)**
Lệnh này mô phỏng tình huống một node bị sập giữa chừng để chứng minh hệ thống tự động bẻ lái (Rerouting) cứu dữ liệu thành công.

```bash
python scenario_failover.py
```
