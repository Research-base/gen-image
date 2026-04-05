import os
from dotenv import load_dotenv
import gradio as gr

from src.ui.interface import build_ui

def main():
    load_dotenv()
    app, theme, css = build_ui()
    # Share=False to keep it in local network. 
    # Can change to True if you want a public link
    app.launch(server_name="0.0.0.0", server_port=7860, theme=theme, css=css)

if __name__ == "__main__":
    main()
