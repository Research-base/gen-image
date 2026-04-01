import torch
from diffusers import StableDiffusionPipeline
import os
import platform

# For Intel hardware (Windows)
try:
    from optimum.intel.openvino import OVStableDiffusionPipeline
    OPENVINO_AVAILABLE = True
except ImportError:
    OPENVINO_AVAILABLE = False

class ModelManager:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5"):
        self.model_id = model_id
        self.device = self._detect_device()
        self.pipe = None
        print(f"[*] Detected device: {self.device}")

    def _detect_device(self):
        """Detect the best available backend."""
        if torch.backends.mps.is_available():
            return "mps"
        elif torch.cuda.is_available():
            return "cuda"
        # On Windows/Linux with Intel, we might use OpenVINO via the pipeline itself.
        # We'll prioritize OpenVINO if we are on a non-Mac, non-CUDA machine.
        if OPENVINO_AVAILABLE and platform.system() != "Darwin":
            return "openvino"
        return "cpu"

    def load_model(self, force_cpu=False):
        """Loads and optimizes the Stable Diffusion model based on device."""
        device = "cpu" if force_cpu else self.device
        
        print(f"[*] Loading model {self.model_id} on {device}...")
        
        if device == "openvino":
            # Save the optimized model locally for faster reuse
            ov_model_path = "./ov_model_sd15"
            if not os.path.exists(ov_model_path):
                print("[!] Exporting model to OpenVINO format (this may take 5-10 mins)...")
                self.pipe = OVStableDiffusionPipeline.from_pretrained(
                    self.model_id, export=True, compile=True
                )
                self.pipe.save_pretrained(ov_model_path)
            else:
                self.pipe = OVStableDiffusionPipeline.from_pretrained(
                    ov_model_path, compile=True
                )
        else:
            # Standard PyTorch (MPS, CUDA, CPU)
            dtype = torch.float16 if device in ["cuda", "mps"] else torch.float32
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id, torch_dtype=dtype
            )
            self.pipe.to(device)

        print("[*] Model loaded successfully.")

    def generate(self, prompt, negative_prompt="", steps=20, guidance_scale=7.5, width=384, height=384):
        """Generates an image from a prompt."""
        if self.pipe is None:
            self.load_model()
            
        print(f"[*] Generating: '{prompt}' | Negative: '{negative_prompt}'")
        
        # Ensure dimensions are multiples of 8 (Requirement for SD)
        width = (width // 8) * 8
        height = (height // 8) * 8
        
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=int(steps),
            guidance_scale=float(guidance_scale),
            width=int(width),
            height=int(height)
        )
        
        return result.images[0]
