# AI Image Generator Lab

Chào mừng bạn đến với **AI Image Generator Lab**! Đây là một ứng dụng giao diện web nhẹ nhàng được viết bằng Python (Gradio) cho phép bạn tự động sinh hình ảnh thông qua các mô hình AI khác nhau. Mục đích chính của công cụ này là đóng vai trò như một phòng thí nghiệm so sánh giữa mô hình Local LLM (như Ollama, SD) và Gemini API.

## 🚀 Các tính năng chính
- **Tuỳ chọn linh hoạt Engine Sinh Ảnh**: Cho phép chuyển đổi linh hoạt việc vẽ ảnh bằng Local Model hay Gemini.
- **Tối Ưu Hoá Cơ Sở (Auto-Enhance)**: Sử dụng mô hình xử lý ngôn ngữ của Gemini để "biến hoá" một câu từ đơn giản thành mô tả hình ảnh cực kỳ chi tiết, giúp AI dễ hiểu.
- **Tuỳ biến Endpoint tự do**: Hỗ trợ gọi API tới một cấu hình URL nội bộ bạn thiết lập (Vd: `http://localhost:11434` của Ollama hay `http://localhost:7860` của ComfyUI/Automatic1111).
- **Tự động lưu trữ**: Ảnh được sinh ra bất kể cấu hình nào đều sẽ được backup tự động về thư mục `images/` trong thư mục gốc.

## ⚙️ Yêu cầu Hệ thống
Bạn cần có cài đặt sẵn `python3` và `pip3` trên máy (thường là mặc định trên MacOS).

## 🛠️ Hướng Dẫn Cài Đặt và Chạy

1. **Thiết lập API Keys**
   Sao chép (hoặc đổi tên) file `.env.example` thành `.env`:
   ```bash
   cp .env.example .env
   ```
   Mở file `.env` bằng trình chỉnh sửa văn bản và dán API Key Gemini của bạn:
   ```env
   GEMINI_API_KEY=phím_api_của_bạn_tại_đây
   ```

2. **Cách cài đặt môi trường:**
   Chạy lệnh sau tại thư mục chứa dự án:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Chạy Phần Mềm:**
   Sau khi quá trình tải thư viện thành công, hãy gõ lệnh khởi động Server:
   ```bash
   python3 app.py
   ```
   Sau đó mở trình duyệt và truy cập: `http://127.0.0.1:7860/`

## 🗂️ Quản Lý Tập Tin
Các hình ảnh được lưu trữ tự động sau mỗi lần gen đều nằm trong thư mục `images/`. Định dạng đặt tên được tối ưu dễ tìm kiếm: `[tên_engine]_[timestamp_chi_tiết].png`
