# 🖼️ Smart AI Image Caption Generator

This is a Streamlit web app that generates captions from images using AI. It uses the BLIP model to describe images, and offers styled captions like **Funny**, **Poetic**, **Aesthetic**, or **Instagram** using either Hugging Face API (if available) or local templates.

## 🔧 Features

- 📤 Upload an image (JPG/PNG)
- 🧠 AI-generated base caption using BLIP
- 🎨 Style the caption into:
  - Funny
  - Poetic
  - Aesthetic
  - Instagram-style
- ✅ Works **offline or online** (auto fallback)
- 🔄 Generate new styled captions with a click

## 🚀 Tech Stack

- Streamlit
- Hugging Face Transformers (BLIP model)
- Optional Hugging Face Inference API
- Python (requests, PIL, torch)

## 📦 Setup

```bash
pip install -r requirements.txt
streamlit run app.py



