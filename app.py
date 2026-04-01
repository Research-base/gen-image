import gradio as gr
from model_manager import ModelManager
import torch
import os

# Initialize the manager
manager = ModelManager()

def generate_image(prompt, negative_prompt, steps, guidance, width, height):
    """Callback function for Gradio button."""
    try:
        image = manager.generate(
            prompt=prompt,
            negative_prompt=negative_prompt,
            steps=steps,
            guidance_scale=guidance,
            width=width,
            height=height
        )
        return image, "Success!"
    except Exception as e:
        return None, f"Error: {str(e)}"

# Define custom CSS for a premium look
css = """
#container { max-width: 1200px; margin: auto; padding-top: 1.5rem; }
.header { text-align: center; margin-bottom: 2rem; }
.sidebar { background: #f8f9fa; padding: 1.5rem; border-radius: 12px; border: 1px solid #e0e0e0; }
.output-img { border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
#generate-btn { background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); color: white; border: none; }
#generate-btn:hover { opacity: 0.9; }
"""

with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_id="container"):
        # Header
        gr.Markdown(
            """
            # 🎨 AI Studio Pro
            ### Create professional images with Stable Diffusion 1.5
            """,
            elem_classes=["header"]
        )
        
        with gr.Row():
            # LEFT: Sidebar Controls
            with gr.Column(scale=1, elem_classes=["sidebar"]):
                prompt = gr.Textbox(
                    label="Prompt", 
                    placeholder="Describe your vision...", 
                    lines=3,
                    info="What do you want to see?"
                )
                negative_prompt = gr.Textbox(
                    label="Negative Prompt", 
                    placeholder="Things to avoid...", 
                    lines=2,
                    info="What do you NOT want to see?"
                )
                
                with gr.Accordion("⚙️ Settings", open=False):
                    steps = gr.Slider(
                        minimum=1, maximum=50, value=20, step=1, 
                        label="Inference Steps",
                        info="More steps = more detail, but slower."
                    )
                    guidance = gr.Slider(
                        minimum=1, maximum=20, value=7.5, step=0.5, 
                        label="Guidance Scale",
                        info="How closely to follow the prompt."
                    )
                    
                    with gr.Row():
                        width = gr.Slider(
                            minimum=256, maximum=768, value=384, step=64, 
                            label="Width"
                        )
                        height = gr.Slider(
                            minimum=256, maximum=768, value=384, step=64, 
                            label="Height"
                        )
                
                generate_btn = gr.Button("Generate Image", variant="primary", elem_id="generate-btn")
                status = gr.Markdown("Status: Ready")

            # RIGHT: Results Gallery
            with gr.Column(scale=2):
                output_image = gr.Image(
                    label="Generated Result", 
                    elem_classes=["output-img"],
                    type="pil",
                    interactive=False
                )
                
                with gr.Row():
                    gr.Markdown("💡 **Tip:** Start with fewer steps (e.g. 15-20) for faster previews.")

        # Interactions
        generate_btn.click(
            fn=generate_image,
            inputs=[prompt, negative_prompt, steps, guidance, width, height],
            outputs=[output_image, status],
        )

if __name__ == "__main__":
    demo.launch(share=False)
