

## 📌 Giới thiệu  
Dự án này được phát triển nhằm giải quyết bài toán crawl dữ liệu từ một website tuyển dụng Đức.  
Mục tiêu là xây dựng một công cụ **scraping dữ liệu việc làm** từ website của [Arbeitsagentur](https://www.arbeitsagentur.de/jobsuche) và chuẩn hóa dữ liệu theo định dạng yêu cầu.  

Ngoài ra, dự án còn mở rộng với các tính năng bonus: lưu dữ liệu vào cơ sở dữ liệu, xử lý thiếu thông tin liên hệ, và tự động giải CAPTCHA.  

---

## 🚀 Chức năng chính  

### 1. Scrape dữ liệu việc làm  
Thu thập thông tin từ nguồn:  
```
https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=4&ausbildungsart=0&arbeitszeit=vz&branche=22;1;2;9;3;5;7;10;11;16;12;21;26;15;17;19;20;8;23;29&veroeffentlichtseit=7&sort=veroeffdatum
```

### 2. Dữ liệu đầu ra  
Thông tin được trích xuất và chuẩn hóa dưới dạng bảng có cấu trúc:  

| Profession | Salary | Company Name | Location | Start Date | Telephone | Email | Job Description | Ref.-Nr. | External Link | Application Link |  

> Một số trường có thể rỗng (ví dụ: Email, Telephone).  

---

## 🎯 Bonus Features (tuỳ chọn)  

1. **Transform & Load Data into Database (hoàn thành)**  
   - Spin up database (local/Docker).  
   - Tạo bảng, transform và lưu dữ liệu scrape được vào DB.  

2. **Handle Missing Emails & Websites (hoàn thành)**  
   - Nếu không có email:  
     - Trích xuất từ Application Link.  
     - Nếu có external link, thử scrape thêm từ `/contact`, `/impressum`, `/kontakt`.  

3. **CAPTCHA Handling (một phần)**  
   - Ban đầu cần giải CAPTCHA thủ công.  
   - Có thể nghiên cứu hướng OCR/ML hoặc dịch vụ bên thứ ba để tự động hoá.  

---

## ⚙️ Công nghệ sử dụng  
- Ngôn ngữ: Python (tuỳ chọn của bạn khi hiện thực)  
- Thư viện sử dụng:  
  - Scraping: `requests`,`Selenium`
  - Database: `PostgreSQL` 
  - CAPTCHA: `pytesseract`, `anti-captcha` API
  - ETL: `Spark` , `Docker`
---

## ▶️ Cách chạy dự án  

1. **Clone repo**  

2. **Cài đặt dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy scraper**  
   ```bash
   python scraping/scraper.py
   ```

4. **Chạy Spark bằng docker**
- Khởi tạo spark cluster
   ```bash
   docker network create streaming-network --driver bridge
   docker build -t unigap/spark:3.5 .
   docker volume create spark_data
   docker volume create spark_lib
   docker compose up -d
   ```
- Khởi tạo spark container để chạy code, lưu ý rằng nên Spark trong dự án này sẽ đọc trên S3, biến đổi sau đó lưu vô postgres nên hãy nhớ đổi S3 path, authen cho postgres, thư mục local mounting lưu trữ các file để container đọc. Lưu ý rằng Access key sẽ không nằm trong code !, chỉ nằm ở trong lúc chạy lệnh dưới thêm -e 
   ```bash
   docker run -ti --name application --user root --network=streaming-network -p 4040:4040 -v "C:\Users\VivoBook\Documents\take_home_assignment\99-project\spark:/spark" -v spark_lib:/opt/bitnami/spark/.ivy2 -v spark_data:/data -e PYSPARK_DRIVER_PYTHON=python -e PYSPARK_PYTHON=./environment/bin/python unigap/spark:3.5 bash -c "mkdir -p /var/lib/apt/lists/partial && apt-get update && apt-get install -y python3-venv python3-pip && python -m venv pyspark_venv --system-site-packages && source pyspark_venv/bin/activate && pip install -r /spark/requirements.txt && venv-pack -o pyspark_venv.tar.gz && spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.postgresql:postgresql:42.7.3 --archives pyspark_venv.tar.gz#environment --py-files /spark/browser.zip /spark/main.py"
```

---

## 📝 Ghi chú  
- Một số job chỉ có **Application Link** hoặc chỉ có **External Link** → đều hợp lệ.  
- CAPTCHA có thể xuất hiện nhiều lần khi scrape nhiều dữ liệu.  
