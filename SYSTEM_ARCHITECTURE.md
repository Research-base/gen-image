# AI SYSTEM ARCHITECTURE & DOCS

Tài liệu này được viết riêng dành cho các Agent AI và lập trình viên (Developer) duy trì dự án. Mục tiêu là giúp AI hiểu được luồng context và các modules sẵn có để bảo trì hoặc nâng cấp ứng dụng Image Generator này.

## 1. Project Organization (Cấu trúc Thư mục)

```text
gen-image/
├── requirements.txt         # Khai báo dependency chính: gradio, requests, google-generativeai, pillow, python-dotenv
├── .env                     # (Ignored) File môi trường lưu GEMINI_API_KEY
├── app.py                   # Điểm khởi tạo dự án (Entry point)
├── images/                  # Nơi lưu trữ tập trung hình ảnh sinh ra
└── src/                     # Source Code chính
    ├── api/                 # Các clients giao tiếp (Network)
    │   ├── local_api.py     # Hỗ trợ parse response chuẩn từ SD WebUI / giải mã base64 Image JSON Ollama
    │   └── gemini_api.py    # Xử lý Prompt Enhancement & Giao tiếp API Google
    ├── ui/                  # Layout/Màn hình
    │   └── interface.py     # Trực tiếp config Gradio Block (Inputs, Parameters)
    └── utils/               # Công cụ bổ trợ
        └── file_mgr.py      # Module lo logic I/O sinh Timestamp String, lưu file Bytes/PIL
```

## 2. Luồng Thực thi Chính (Primary Flows)

### Flow Sinh Ảnh: `process_generate` (tại `interface.py`)
Hàm đóng vai trò Brain kết nối UI và Logic. Hoạt động:
1. Đọc params từ UI Gradio.
2. Kiểm tra cờ rẽ nhánh `auto_enhance`. Nếu = True, gọi hàm `enhance_prompt_with_gemini()`.
3. Kiểm tra biến đổi Engine (`Local Model` vs `Gemini`):
   - Nhánh `Local`: Chuyển Request cho `generate_local_image()` tại local_api.py -> Nhận `PIL.Image`.
   - Nhánh `Gemini`: Chuyển Request cho `generate_gemini_image()` tại gemini_api.py.
4. Xử lý Logic File I/O: Khi trả về Object `PIL.Image` thành công, truyền object qua hàm `save_pil_image()` tại file_mgr.py để tự động backup ra bộ lưu trữ cục bộ thư mục `/images/`.

### Kỹ thuật xử lý Local Response `local_api.py`
Vì Local API có thể là một server Standalone (A1111/ComfyUI) hoặc là Ollama Gen (Ví dụ Flux model):
- Hàm chủ động kiểm tra endpoint string URL (`is_ollama = "11434" in api_url ...`).
- Nếu là Ollama: Extract nội dung trường JSON `response` và cố gắng dùng Regex decode dạng biểu diễn Base64 Image. 
- Nếu là SD Standard: Gọi và Extract nội dung array JSON `images[0]`.

### Kỹ thuật xử lý Gemini API `gemini_api.py`
- Hàm `enhance_prompt_with_gemini`: Tận dụng mô hình siêu ngôn ngữ `gemini-1.5-flash` đóng vai trò "Prompt engineer". Model nhận input, áp logic prompt format, và sinh ra payload text.
- Hàm `generate_gemini_image`: Sử dụng backend Vertex Endpoint `imagen-3.0-generate-001` cấu hình dạng HTTP POST call thông qua thư viện `requests` vì SDK standard chưa bao phủ trọn vẹn endpoint Imagen này. Response giải mã tương tự trên mảng `predictions`.

## 3. Quy Ước Code (Code Convention & Maintenance)
- **Typing Hints:** Các hàm được khai báo Python Typing Hints hỗ trợ rõ IDE (Ví dụ: `engine_name: str`).
- **Gradio Update:** Bắt buộc duy trì cú pháp share inputs thành single array vào hàm Call (Ví dụ tại `fn=process_generate`).
- **Lưu ý Thư viện:** Luôn dùng `python3` để phát triển, khuyến nghị người dùng dùng `pip3` khi upgrade packages hệ thống này nhằm tránh confict mac-os environment cục bộ.

Khi nhận request thêm tính năng, Agent có thể an tâm read/write các file trong nội bộ `src/` tuỳ ý dựa theo bản đồ phía trên. Mọi tính năng I/O (Lưu trữ data ảnh/byte) bắt buộc đưa về `utils/file_mgr.py` để quản lý.
