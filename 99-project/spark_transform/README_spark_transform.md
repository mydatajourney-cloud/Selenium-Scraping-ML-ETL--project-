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
├── docker-compose_yml    # Khởi tạo spark cluster
│
├── browser/
│   ├── utils.py        # Gồm các hàm chạy biến đổi, chuẩn hoá và làm sạch dữ liệu
│   ├── config.py      # File để parse spark config
│   ├── log.py           # Tạo log
│
├──  main.py           # File code chính, khởi tạo spark context
├──  spark.conf        # File cấu hình spark context 
│
├── README_spark_transform.md             # Tài liệu giới thiệu dự án
```

## ⚙️ Các file chính

### 1. `main.py`  
- Khởi tạo spark context và thực hiện chạy ETL

### 2. `utils.py`  
- Thực hiện các bước transform:  
  - Loại bỏ các chữ crawl thừa
  - Biến đổi range salary thành dạng số
  - Chuẩn hoá array Emails, Telephone  
  - Đưa dữ liệu chuẩn hoá vào postgres 
### 3. `config.py`  
- File hỗ trợ parse spark config 

---

## 🎯 Kết quả đạt được
- Dữ liệu thô ban đầu được **chuẩn hoá và làm sạch** bằng Spark  
- Kết quả đầu ra sẽ đi vào **postgres**, tuy nhiên dữ liệu kết quả output sẽ được mô tả ở trong thư mục:
```
data/output/
---

## ▶️ Cách chạy pipeline
-- Cách chạy đã được giới thiệu ở mục Readme đầu trang 
---

## 📝 Ghi chú
- Thích hợp cho xử lý dữ liệu vừa & lớn bằng Spark  
- Có thể mở rộng để chạy trên cluster thật (YARN, Kubernetes, EMR) thay vì local  
