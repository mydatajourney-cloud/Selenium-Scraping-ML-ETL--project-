# ML_captcha 🔐🖼️

## 📌 Giới thiệu
`ML_captcha` là một dự án demo tập trung vào **xử lý ảnh CAPTCHA** trước khi đưa vào mô hình Machine Learning.  
Mục tiêu là làm sạch và chuẩn hoá captcha (loại bỏ nhiễu, chuyển sang grayscale, threshold, segmentation, v.v.) để tăng độ chính xác khi nhận diện.  

---

## 📂 Cấu trúc dự án
```
ML_captcha/
├── data/
│   ├── raw/             # Ảnh captcha gốc
│   └── processed/       # Ảnh captcha sau khi xử lý
│
├── src/
│   ├── preprocess.py    # Chứa pipeline xử lý captcha
│   ├── visualize.py     # Hiển thị kết quả so sánh trước & sau
│
├── README.md            # Tài liệu dự án
├── requirements.txt     # Thư viện cần thiết
```

---

## ⚙️ Các bước xử lý captcha
Pipeline trong `preprocess.py` gồm:
1. **Chuyển grayscale** – giảm kênh màu → tập trung vào ký tự.  
2. **Threshold / Binarization** – tách nền khỏi chữ.  
3. **Loại bỏ nhiễu** – làm sạch pixel thừa.  
4. **Segmentation (tuỳ chọn)** – cắt captcha thành từng ký tự riêng.  
5. **Resize** – chuẩn hoá kích thước đầu vào cho mô hình.  

---

## ▶️ Cách chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy script xử lý
```bash
python src/preprocess.py --input ./data/raw/0001.png --output ./data/processed/0001_clean.png
```

### 3. Hiển thị kết quả
```bash
python src/visualize.py --input ./data/raw/0001.png
```

Kết quả hiển thị ví dụ:  

| Ảnh gốc | Ảnh sau xử lý |
|---------|---------------|
| ![raw](./data/raw/0001.png) | ![processed](./data/processed/0001_clean.png) |

---

## 📝 Ghi chú
- Kết quả preprocessing có thể tuỳ chỉnh bằng cách thay đổi ngưỡng threshold hoặc kernel lọc nhiễu.  
- Nếu captcha có nền phức tạp, có thể kết hợp thêm **morphological operations (erosion/dilation)**.  
- Thư viện chính: `opencv-python`, `numpy`, `matplotlib`.  
