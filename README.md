## 🚀 Quick Start (Recommended: Use Virtual Environment)

### 1. Setup Virtual Environment (Keep your system clean)
**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```
**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app (ensure venv is active)
```bash
python app.py
```

## 🛠️ System Architecture (For AI/Devs)
- **Framework**: `Gradio` (Front-end), `Diffusers`/`Optimum` (Back-end).
- **Backend Selection**:
    - **Apple M-Series**: Automatically uses `mps` device via `diffusers.DiffusionPipeline`.
    - **Windows Intel GPU**: Uses `OVStableDiffusionPipeline` from `optimum.intel`. Exports model to `./ov_model_sd15` for persistent optimization.
    - **Fallback**: Standard PyTorch CPU.
- **Model**: Stable Diffusion v1.5 (`runwayml/stable-diffusion-v1-5`).
- **Core Files**:
    - `app.py`: UI Layout (Gradio Blocks) and event handling.
    - `model_manager.py`: Hardware detection and image generation logic.
    - `requirements.txt`: Unified dependencies for all platforms.

## ⚙️ Default Configurations
- **Resolution**: 384x384 (Default for performance), adjustable up to 768x768.
- **Inference Steps**: 20 (Balanced speed/quality).
- **Guidance Scale**: 7.5.

## ⚠️ Notes for Intel Users
The first run on Windows will take **5-10 minutes** as it converts the model to OpenVINO format. Subsequent runs will start instantly.
