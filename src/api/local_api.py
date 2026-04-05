import requests
import json
import base64
import re
from PIL import Image
from io import BytesIO

def generate_local_image(api_url: str, model_name: str, prompt: str, neg_prompt: str, width: int, height: int, steps: int, cfg_scale: float, seed: int):
    """
    Sends a request to local API (Ollama or SD WebUI).
    Returns a PIL Image object or None, and an error string if any.
    """
    if not api_url:
        return None, "API URL is empty"
    
    # Try to detect if it's Ollama or SD WebUI based on URL endpoint
    is_ollama = "11434" in api_url or "/api/generate" in api_url
    
    try:
        if is_ollama:
            # Payload matching Ollama API (/api/generate schema)
            # Ollama x/flux2-klein might output base64 encoded image directly in 'response'
            options = {
                "temperature": cfg_scale / 10.0 # using cfg as a mock proxy if needed
            }
            if seed != -1:
                options["seed"] = int(seed)

            payload = {
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                # Additional params for inference (if model supports it)
                "options": options
            }
            response = requests.post(api_url, json=payload, timeout=600)
            response.raise_for_status()
            
            data = response.json()
            
            # Ollama image generation models often return base64 in "image" or "images" key.
            # Fallback to checking "response" text.
            b64_str = ""
            if "image" in data and str(data["image"]).strip():
                b64_str = data["image"]
            elif "images" in data and len(data["images"]) > 0:
                b64_str = data["images"][0]
            else:
                result_text = data.get("response", "")
                b64_match = re.search(r"base64,([A-Za-z0-9+/=]+)", result_text)
                if b64_match:
                    b64_str = b64_match.group(1)
                else:
                    b64_str = result_text.strip()
                
            try:
                img_data = base64.b64decode(b64_str)
                img = Image.open(BytesIO(img_data))
                return img, None
            except Exception as e:
                return None, f"Could not decode Image Base64 from Ollama. Ensure model specifically generates images. Raw text chunk: {str(b64_str)[:100]}..."
        
        else:
            # Assume SD WebUI API (e.g. http://127.0.0.1:7860/sdapi/v1/txt2img)
            payload = {
                "prompt": prompt,
                "negative_prompt": neg_prompt,
                "width": width,
                "height": height,
                "steps": steps,
                "cfg_scale": cfg_scale,
                "seed": seed
            }
            # Add dynamic model change if specified
            if model_name:
                payload["override_settings"] = {"sd_model_checkpoint": model_name}

            response = requests.post(api_url, json=payload, timeout=600)
            response.raise_for_status()
            data = response.json()
            images = data.get("images", [])
            if images:
                img_data = base64.b64decode(images[0])
                img = Image.open(BytesIO(img_data))
                return img, None
            else:
                return None, "No image returned from Local WebUI"
                
    except Exception as e:
        return None, f"Local API Error: {str(e)}"
