# 🖼️ AI Image Caption Generator

This app generates a caption for any uploaded image using BLIP and rewrites it in a creative style using a Hugging Face model.

## 🔧 Tech Stack

- Streamlit
- Hugging Face Transformers
- Salesforce BLIP (for base captions)
- Falcon-7B-Instruct (for caption stylizing)

## 🚀 How to Run

1. Clone the repo or upload to GitHub.
2. Add your Hugging Face API token to `.streamlit/secrets.toml`
3. Run the app locally:
   ```bash
   streamlit run app.py
   ```
4. Or deploy it via [Streamlit Cloud](https://streamlit.io/cloud).

## ✨ Features

- Upload image (JPG, PNG)
- Choose from 4 creative styles
- Get a base caption + stylized version