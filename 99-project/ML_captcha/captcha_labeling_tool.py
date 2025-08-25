import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import csv

# thư mục chứa captcha
IMAGE_DIR = "images"
OUTPUT_FILE = "labels.csv"

# load danh sách ảnh
images = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
images.sort()

current_index = 0

# nếu chưa có file labels.csv thì tạo
if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "label"])


def load_image(index):
    """Load ảnh theo index"""
    img_path = os.path.join(IMAGE_DIR, images[index])
    pil_img = Image.open(img_path)
    pil_img = pil_img.resize((200, 80))  # resize nhỏ cho dễ nhìn
    return ImageTk.PhotoImage(pil_img)


def save_label(event=None):
    """Lưu label và chuyển sang ảnh tiếp theo"""
    global current_index
    label = entry.get().strip()
    if label:
        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([images[current_index], label])
        entry.delete(0, tk.END)

        current_index += 1
        if current_index < len(images):
            update_image()
        else:
            status_label.config(text="Xong hết rồi 🎉")
            entry.config(state="disabled")
            button.config(state="disabled")


def update_image():
    """Hiển thị ảnh mới"""
    global tk_img
    tk_img = load_image(current_index)
    img_label.config(image=tk_img)
    status_label.config(text=f"Ảnh {current_index+1}/{len(images)}: {images[current_index]}")
    entry.focus()


# === GUI ===
root = tk.Tk()
root.title("Captcha Labeling Tool")

# hiển thị ảnh
tk_img = load_image(current_index)
img_label = tk.Label(root, image=tk_img)
img_label.pack(pady=10)

# ô nhập text
entry = ttk.Entry(root, font=("Arial", 16))
entry.pack(pady=5)
entry.bind("<Return>", save_label)  # nhấn Enter để lưu

# nút lưu
button = ttk.Button(root, text="Lưu", command=save_label)
button.pack(pady=5)

# status
status_label = tk.Label(root, text="")
status_label.pack()

update_image()

root.mainloop()
