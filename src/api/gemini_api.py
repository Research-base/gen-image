import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import requests

def generate_gemini_image(prompt: str, api_key: str, model_name: str = "imagen-4.0-generate-001"):
    """
    Attempts to generate an image using Gemini API (Rest fallback to imagen-3.0).
    """
    if not api_key:
        return None, "Gemini API key is not set. Check your .env file."
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:predict?key={api_key}"
        payload = {
            "instances": [
                {
                    "prompt": prompt
                }
            ],
            "parameters": {
                "sampleCount": 1
            }
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            predictions = data.get("predictions", [])
            if predictions and "bytesBase64Encoded" in predictions[0]:
                import base64
                b64_str = predictions[0]["bytesBase64Encoded"]
                img_data = base64.b64decode(b64_str)
                img = Image.open(BytesIO(img_data))
                return img, None
            else:
                return None, "No image found in prediction response."
        else:
            return None, f"Gemini API Error: {response.text}"
            
    except Exception as e:
        return None, f"Error calling Gemini API: {str(e)}"

def enhance_prompt_with_gemini(prompt: str, api_key: str):
    """
    Use Gemini Text model to enrich the prompt for better text-to-image quality.
    """
    if not api_key:
        return prompt, "API key not found"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        instruction = "You are an expert prompt engineer for Stable Diffusion/Midjourney. Enhance the following base prompt into a highly detailed, comma-separated image generation prompt. Add descriptors for lighting, art style, details, and quality (e.g., sharp focus, 8k, masterpiece). Output ONLY the final prompt itself."
        response = model.generate_content(f"{instruction}\n\nBase prompt: {prompt}")
        return response.text.strip(), None
    except Exception as e:
        return prompt, str(e)
