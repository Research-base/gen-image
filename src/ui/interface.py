import gradio as gr
import os
from dotenv import load_dotenv

from src.utils.file_mgr import save_pil_image
from src.api.local_api import generate_local_image
from src.api.gemini_api import generate_gemini_image, enhance_prompt_with_gemini

load_dotenv()

def process_generate(prompt, engine, local_url, local_model, neg_prompt, width, height, steps, cfg_scale, seed, auto_enhance):
    # Lấy key trong hàm để cập nhật hot-reload nếu pass key
    GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
    
    if not prompt.strip():
        return None, "", "Error: Prompt is empty."
        
    final_prompt = prompt
    status = ""
    
    if auto_enhance:
        enhanced, err = enhance_prompt_with_gemini(prompt, GEMINI_KEY)
        if not err:
            final_prompt = enhanced
            status += "Prompt Enhanced.\n"
        else:
            status += f"Enhance Failed: {err}\n"
            
    img = None
    err = None
    
    if engine == "Local Model":
        img, err = generate_local_image(local_url, local_model, final_prompt, neg_prompt, width, height, steps, cfg_scale, seed)
    elif engine == "Gemini":
        img, err = generate_gemini_image(final_prompt, GEMINI_KEY)
    else:
        err = "Engine not supported."
        
    if err:
        return None, final_prompt, f"{status}Error: {err}"
        
    if img:
        saved_path = save_pil_image(img, "local" if engine == "Local Model" else "gemini")
        return img, final_prompt, f"{status}Success! Saved to {saved_path}"
    
    return None, final_prompt, f"{status}No image generated."

def build_ui():
    # Khởi tạo custom theme chuyên nghiệp hơn
    custom_theme = gr.themes.Soft(
        primary_hue="violet",
        secondary_hue="indigo",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    ).set(
        body_background_fill="linear-gradient(to right bottom, #f8fafc, #e2e8f0)",
        block_background_fill="*background_fill_primary",
        block_radius="xl",
        block_shadow="*shadow_drop_lg",
        button_primary_background_fill="linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%)",
        button_primary_background_fill_hover="linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%)",
        button_primary_text_color="white",
        button_primary_shadow="0 4px 6px -1px rgba(124, 58, 237, 0.4)",
    )
    
    # Custom CSS cho Container gọn gàng
    custom_css = """
    .main-container { max-width: 1200px !important; margin: 0 auto; padding-top: 20px; }
    h1 { background: -webkit-linear-gradient(45deg, #4f46e5, #9333ea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0 !important; }
    .header-text { margin-top: 5px; color: #64748b; font-size: 1.1em; }
    """

    with gr.Blocks(title="AI Image Generator Lab") as app:
        with gr.Column(elem_classes="main-container"):
            gr.Markdown("<h1 style='text-align: center; font-weight: 800; font-size: 3em;'>✨ AI Image Generator Lab</h1>")
            gr.Markdown("<p class='header-text' style='text-align: center;'>Phòng lab thử nghiệm gen ảnh sử dụng AI tạo sinh (Ollama, SD WebUI, Gemini Imagen).</p>")
            gr.Markdown("---")
            
            with gr.Row(equal_height=False):
                # Left column: Setup and Parameters
                with gr.Column(scale=4):
                    gr.Markdown("### ⚙️ Cấu Hình & Tham Số")
                    
                    with gr.Group():
                        engine = gr.Radio(["Local Model", "Gemini"], label="🤖 Lõi Xử Lý (Active Engine)", value="Local Model", interactive=True)
                        
                        with gr.Accordion("🔌 Local Model Settings", open=True):
                            local_url = gr.Textbox(label="API URL", value="http://localhost:11434/api/generate", info="VD: Ollama (/api/generate) hoặc SD WebUI (http://127.0.0.1:7860/sdapi/v1/txt2img)")
                            local_model = gr.Textbox(label="Model Name", value="x/flux2-klein:9b", info="Tên model chạy trên Local (VD: x/flux2-klein:9b)")
                    
                    with gr.Group():
                        prompt = gr.Textbox(label="✍️ Khơi Gợi Nội Dung (Prompt)", lines=4, placeholder="A futuristic city in cyberpunk style, neon lights reflections, hyperrealistic...")
                        auto_enhance = gr.Checkbox(label="✨ Auto-Enhance Prompt with Gemini (Làm giàu ngôn từ mô tả)", value=False)
                        neg_prompt = gr.Textbox(label="🛑 Mô tả Loại Trừ (Negative Prompt - chỉ Local)", lines=2, placeholder="blurry, bad anatomy, bad quality, grainy...")
                    
                    with gr.Accordion("🎛️ Nâng Cao (Generation Parameters)", open=False):
                        with gr.Row():
                            width = gr.Slider(256, 2048, 1024, step=64, label="Chiều rộng (Width)")
                            height = gr.Slider(256, 2048, 1024, step=64, label="Chiều cao (Height)")
                        with gr.Row():
                            steps = gr.Slider(1, 150, 20, step=1, label="Số vòng lặp (Steps)")
                            cfg_scale = gr.Slider(1.0, 30.0, 7.0, step=0.5, label="Bám sát mô tả (CFG Scale)")
                        seed = gr.Number(label="Hạt giống ngẫu nhiên (Seed | -1 là random)", value=-1)
                    
                    generate_btn = gr.Button("🚀 BẮT ĐẦU TẠO ẢNH", variant="primary", size="lg")
                
                # Right column: Output and Comparison
                with gr.Column(scale=6):
                    gr.Markdown("### 🖼️ Kết Quả (Result)")
                    output_image = gr.Image(label="Ảnh Trả Về", type="pil", interactive=False, elem_id="output-img", height=500)
                    
                    with gr.Group():
                        status_out = gr.Textbox(label="Trạng Thái (Status)", interactive=False, lines=1)
                        final_prompt_out = gr.Textbox(label="Prompt Đã Dùng (Final Used Prompt)", interactive=False, lines=3)
                    
        generate_btn.click(
            fn=process_generate,
            inputs=[prompt, engine, local_url, local_model, neg_prompt, width, height, steps, cfg_scale, seed, auto_enhance],
            outputs=[output_image, final_prompt_out, status_out]
        )
        
    return app, custom_theme, custom_css
