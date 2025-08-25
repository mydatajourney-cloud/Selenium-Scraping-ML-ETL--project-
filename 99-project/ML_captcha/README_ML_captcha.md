# ML_captcha 🔐🖼️

## 📌 Giới thiệu
`ML_captcha` là một dự án demo tập trung vào **xử lý ảnh CAPTCHA** trước khi đưa vào mô hình Machine Learning.  
Mục tiêu là làm sạch và chuẩn hoá captcha (loại bỏ nhiễu, chuyển sang grayscale, threshold, segmentation, v.v.) để tăng độ chính xác khi nhận diện.  
Sau đó so sánh sự hiệu quả của phương pháp với việc không sử lý thì kết quả như thế nào

## ⚙️ Các bước xử lý captcha
Pipeline trong `preprocess.py` gồm:
1. **Chuyển grayscale** – giảm kênh màu → tập trung vào ký tự.  
2. **Threshold** – tách nền khỏi chữ.  
3. **Loại bỏ nhiễu** – làm sạch pixel thừa.  
5. **Resize** – chuẩn hoá kích thước đầu vào cho mô hình.  

---

## ▶️ Cách chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy script xử lý
```bash
Thực hiện chạy các code ở trong file .ipynb. 
```

## Mở rộng
### Tạo file labels cho từng file ảnh 
```bash
python captcha_labeling_tool.py
```
## 📝 Ghi chú
- Kết quả preprocessing có thể tuỳ chỉnh bằng cách thay đổi ngưỡng threshold hoặc kernel lọc nhiễu.  
- Nếu captcha có nền phức tạp, có thể kết hợp thêm **morphological operations (erosion/dilation)**.  
- Thư viện chính: `opencv-python`, `numpy`, `matplotlib`.  
