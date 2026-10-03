# 📝 TaskFlow - Flask To-Do List Web Application

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-black.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite3-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TaskFlow** là một ứng dụng web quản lý công việc (To-Do List) được xây dựng bằng **Python Flask** và **SQLite**. Ứng dụng sở hữu giao diện hiện đại, tối ưu trải nghiệm người dùng với đầy đủ các tính năng CRUD, phân loại theo danh mục, quản lý mức độ ưu tiên, hạn chót (deadline) và thanh thống kê tiến độ trực quan.

Dự án được cấu trúc gọn gàng, chuẩn mực và sẵn sàng để đăng lên GitHub làm đồ án mini / portfolio cá nhân.

---

## ✨ Tính Năng Nổi Bật

- 📋 **Quản lý công việc toàn diện (CRUD):** Thêm mới, xem danh sách, chỉnh sửa chi tiết và xóa công việc.
- 🎯 **Phân loại & Mức độ ưu tiên:**
  - Hỗ trợ gắn nhãn danh mục (*Học tập, Công việc, Cá nhân, Dự án...*).
  - 3 cấp độ ưu tiên với màu sắc nhận diện (*Cao 🔴, Trung bình 🟡, Thấp 🟢*).
- ⏰ **Hạn chót & Nhận diện Deadline thông minh:**
  - Tự động tính toán và cảnh báo công việc: *Quá hạn (màu đỏ)*, *Đến hạn hôm nay (màu vàng)*, hoặc số ngày còn lại.
- 🔍 **Tìm kiếm & Bộ lọc linh hoạt:**
  - Tìm kiếm nhanh theo tiêu đề hoặc ghi chú mô tả.
  - Lọc theo trạng thái: *Tất cả*, *Đang làm*, *Đã hoàn thành*.
  - Lọc theo từng danh mục riêng biệt.
- 📊 **Thống kê & Tiến độ thời gian thực:**
  - Dashboard hiển thị tổng số việc, số việc đang thực hiện, việc đã hoàn thành.
  - Thanh tiến độ (Progress bar) tự động cập nhật tỷ lệ hoàn thành (%).
- ⚡ **Tương tác mượt mà (AJAX):**
  - Đánh dấu hoàn thành việc làm tức thì mà không cần load lại trang.
- 🧹 **Dọn dẹp nhanh:** Nút bấm xóa hàng loạt các công việc đã hoàn thành chỉ với 1 click.

---

## 🛠️ Công Nghệ Sử Dụng

| Thành phần | Công nghệ |
| :--- | :--- |
| **Backend** | Python 3, Flask framework |
| **Database** | SQLite3 (tích hợp sẵn trong Python, không cần cài đặt thêm server DB) |
| **Frontend** | HTML5, CSS3, JavaScript (Fetch API) |
| **UI Library** | Bootstrap 5.3, Bootstrap Icons, Google Fonts (Plus Jakarta Sans) |

---

## 📁 Cấu Trúc Thư Mục

```text
todo-flask-app/
├── app.py              # File chính chạy ứng dụng Flask & điều hướng routes
├── database.py         # Module quản lý kết nối và truy vấn SQLite
├── requirements.txt    # Danh sách các thư viện cần cài đặt
├── .gitignore          # Cấu hình bỏ qua các file tạm, cache khi đẩy lên git
├── README.md           # Hướng dẫn chi tiết dự án
├── LICENSE             # Giấy phép mã nguồn mở (MIT)
├── static/
│   ├── css/
│   │   └── style.css   # Giao diện tùy chỉnh, hiệu ứng thẻ và màu sắc
│   └── js/
│       └── main.js     # Xử lý tương tác AJAX và hiệu ứng client-side
└── templates/
    ├── base.html       # Layout dùng chung (Navbar, Footer, CSS/JS CDN)
    ├── index.html      # Trang chủ (Dashboard, Form thêm, Danh sách việc)
    └── edit.html       # Trang chỉnh sửa công việc
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Ứng Dụng

### 1. Chuẩn bị môi trường

Đảm bảo máy bạn đã cài đặt **Python 3.8+** và **Git**.

### 2. Cài đặt thư viện

Mở Terminal / PowerShell tại thư mục dự án `todo-flask-app`:

```bash
# Khuyến nghị tạo môi trường ảo (tùy chọn)
python -m venv .venv

# Kích hoạt môi trường ảo (trên Windows)
.venv\Scripts\activate

# Cài đặt Flask
pip install -r requirements.txt
```

### 3. Khởi chạy ứng dụng

```bash
python app.py
```

Sau khi chạy lệnh trên, mở trình duyệt web và truy cập địa chỉ:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

Database `todos.db` sẽ tự động được khởi tạo cùng với một số dữ liệu mẫu ban đầu.

---

## 📤 Hướng Dẫn Đẩy Project Lên GitHub

Làm theo các bước đơn giản sau để đăng dự án này lên GitHub:

### Bước 1: Tạo Repository mới trên GitHub
1. Đăng nhập vào tài khoản [GitHub](https://github.com).
2. Nhấn nút **New repository** (hoặc dấu `+` ở góc trên bên phải).
3. Đặt tên repository: `flask-todo-app` (hoặc tên bạn thích).
4. Để chế độ **Public**.
5. **Không** tích chọn *"Add a README file"* (vì dự án đã có sẵn).
6. Nhấn **Create repository**.

### Bước 2: Đẩy mã nguồn từ máy lên GitHub
Mở PowerShell tại thư mục `todo-flask-app` và chạy tuần tự các lệnh sau:

```bash
# 1. Khởi tạo Git trong thư mục dự án
git init

# 2. Thêm tất cả các file vào Git
git add .

# 3. Tạo commit đầu tiên
git commit -m "feat: Initial commit with Flask To-Do App"

# 4. Đổi tên nhánh mặc định thành main
git branch -M main

# 5. Liên kết với kho chứa trên GitHub (thay URL bằng link repo GitHub của bạn)
git remote add origin https://github.com/<tai-khoan-cua-ban>/flask-todo-app.git

# 6. Đẩy code lên GitHub
git push -u origin main
```

---

## 📜 Giấy Phép (License)

Dự án này được phát hành dưới giấy phép [MIT License](LICENSE). Bạn hoàn toàn có thể tự do sử dụng, chỉnh sửa và phát triển thêm.
