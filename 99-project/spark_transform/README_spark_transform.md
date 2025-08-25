# spark_transform ⚡🐍

## 📌 Giới thiệu
`spark_transform` là một dự án minh hoạ **ETL pipeline với Apache Spark**.  
Mục tiêu là **load dữ liệu thô**, **transform bằng Spark**, và **xuất kết quả cuối cùng** ở định dạng đã chuẩn hoá, có thể dùng cho phân tích hoặc đưa vào hệ thống downstream.

---

## 📂 Cấu trúc dự án
```
spark_transform/
├── Dockerfile            # Docker hoá môi trường Spark + Python
├── requirements.txt      # Các thư viện Python cần thiết
│
├── src/
│   ├── extract.py        # Bước Extract: tải / đọc dữ liệu từ nguồn (CSV, API, DB)
│   ├── transform.py      # Bước Transform: làm sạch, chuẩn hoá, join, enrich dữ liệu
│   ├── load.py           # Bước Load: ghi dữ liệu kết quả ra file (parquet, csv) hoặc DB
│
├── data/
│   ├── input/            # Dữ liệu gốc (raw data)
│   └── output/           # Dữ liệu sau khi transform
│
├── README.md             # Tài liệu giới thiệu dự án
```

---

## 🐳 Dockerfile
`Dockerfile` giúp khởi chạy môi trường đồng nhất, gồm:
- Cài đặt **Apache Spark + Hadoop** (phiên bản lightweight cho local cluster)
- Python runtime + thư viện cần thiết (`pyspark`, `pandas`, v.v.)
- Thiết lập working directory `/app`

Cách build & run:
```bash
docker build -t spark_transform .
docker run -it --rm -v $(pwd):/app spark_transform
```

---

## ⚙️ Các file chính

### 1. `extract.py`  
- Đọc dữ liệu đầu vào từ `./data/input/` (ví dụ: CSV, JSON, API)  
- Chuẩn hoá định dạng thành **Spark DataFrame**  

### 2. `transform.py`  
- Thực hiện các bước transform:  
  - Loại bỏ giá trị null / trùng lặp  
  - Chuyển đổi kiểu dữ liệu  
  - Join dữ liệu từ nhiều bảng  
  - Tạo thêm cột tính toán mới (ví dụ: tổng, trung bình, phân loại)  

### 3. `load.py`  
- Lưu dữ liệu transform ra thư mục `./data/output/`  
- Hỗ trợ nhiều định dạng: **Parquet, CSV, JSON**  
- Có thể mở rộng để load vào DB (Postgres, BigQuery, v.v.)  

---

## 🎯 Kết quả đạt được
- Dữ liệu thô ban đầu được **chuẩn hoá và làm sạch** bằng Spark  
- Kết quả đầu ra nằm trong thư mục:
```
data/output/
```
Ví dụ:
```bash
data/output/cleaned_data.parquet
data/output/summary.csv
```

> Sau khi transform, dữ liệu có thể dùng ngay cho **phân tích BI**, **ML training pipeline**, hoặc **nạp vào data warehouse**.

---

## ▶️ Cách chạy pipeline

1. **Chạy Extract**  
```bash
python src/extract.py
```

2. **Chạy Transform**  
```bash
python src/transform.py
```

3. **Chạy Load**  
```bash
python src/load.py
```

> Có thể kết hợp thành pipeline ETL hoàn chỉnh, ví dụ trong `Makefile` hoặc Airflow DAG.

---

## 📝 Ghi chú
- Thích hợp cho xử lý dữ liệu vừa & lớn bằng Spark  
- Có thể mở rộng để chạy trên cluster thật (YARN, Kubernetes, EMR) thay vì local  
- Tối ưu khi dữ liệu input ở dạng **Parquet/ORC**  
