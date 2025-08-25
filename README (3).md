# HireLinks Job Scraper

## 📌 Giới thiệu  
Dự án này được phát triển nhằm giải quyết **take-home assignment** của HireLinks.  
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

1. **Transform & Load Data into Database**  
   - Spin up database (local/Docker).  
   - Tạo bảng, transform và lưu dữ liệu scrape được vào DB.  

2. **Handle Missing Emails & Websites**  
   - Nếu không có email:  
     - Trích xuất từ Application Link.  
     - Nếu có external link, thử scrape thêm từ `/contact`, `/impressum`, `/kontakt`.  

3. **CAPTCHA Handling**  
   - Ban đầu cần giải CAPTCHA thủ công.  
   - Có thể nghiên cứu hướng OCR/ML hoặc dịch vụ bên thứ ba để tự động hoá.  

---

## ⚙️ Công nghệ sử dụng  
- Ngôn ngữ: Python / Node.js / (tuỳ chọn của bạn khi hiện thực)  
- Thư viện gợi ý:  
  - Scraping: `requests`, `BeautifulSoup`, `Selenium`, `Playwright`  
  - Database: `PostgreSQL / MySQL / SQLite`  
  - ORM: `SQLAlchemy` hoặc `Prisma`  
  - CAPTCHA: `pytesseract`, `anti-captcha` API  

---

## 📂 Cấu trúc dự án (gợi ý)  
```
├── src/
│   ├── scraper.py       # Logic scrape dữ liệu
│   ├── parser.py        # Chuẩn hoá dữ liệu
│   ├── db.py            # Kết nối & load vào database
│   ├── utils.py         # Xử lý email, link liên hệ
├── requirements.txt     # Thư viện Python
├── Dockerfile           # Nếu chạy trong container
├── README.md            # Tài liệu dự án
```

---

## ▶️ Cách chạy dự án  

1. **Clone repo**  
   ```bash
   git clone https://github.com/<your-username>/hirelinks-job-scraper.git
   cd hirelinks-job-scraper
   ```

2. **Cài đặt dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy scraper**  
   ```bash
   python src/scraper.py
   ```

4. **(Tuỳ chọn) Load vào DB**  
   ```bash
   python src/db.py
   ```

---

## 📝 Ghi chú  
- Một số job chỉ có **Application Link** hoặc chỉ có **External Link** → đều hợp lệ.  
- CAPTCHA có thể xuất hiện nhiều lần khi scrape nhiều dữ liệu.  
