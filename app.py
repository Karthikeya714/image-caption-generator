import streamlit as st
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch
import requests
import time
import random
import re

# Try to load Hugging Face API key (optional now)
try:
    HF_API_TOKEN = st.secrets["hf_api_token"]
    USE_API = True
except:
    HF_API_TOKEN = None
    USE_API = False
    st.info("💡 Running in offline mode - using built-in caption styling")

# === Load BLIP model for image captioning ===
@st.cache_resource
def load_blip_model():
    try:
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        return processor, model
    except Exception as e:
        st.error(f"Error loading BLIP model: {e}")
        return None, None

processor, model = load_blip_model()

# === Streamlit UI ===
st.set_page_config(page_title="Smart AI Caption Generator", layout="centered")
st.title("🖼️ Smart AI Image Caption Generator")
st.markdown("Upload an image and generate funny, poetic, or aesthetic captions using AI!")

uploaded_file = st.file_uploader("📤 Upload your image", type=["jpg", "jpeg", "png"])
caption_style = st.selectbox("🎨 Choose caption style", ["Funny", "Poetic", "Aesthetic", "Instagram"])

# === Generate basic caption using BLIP ===
def generate_blip_caption(image):
    if processor is None or model is None:
        return "a beautiful moment captured"
    
    try:
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs, max_length=50, num_beams=4)
        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption
    except Exception as e:
        return "a beautiful scene"

# === Advanced caption styling (works offline) ===
def create_advanced_caption(blip_caption, style):
    """Advanced caption generation with multiple variations"""
    
    # Clean up the caption
    caption = blip_caption.lower().strip()
    
    # Extract key elements
    words = caption.split()
    
    style_generators = {
        "Funny": generate_funny_caption,
        "Poetic": generate_poetic_caption,
        "Aesthetic": generate_aesthetic_caption,
        "Instagram": generate_instagram_caption
    }
    
    generator = style_generators.get(style, generate_instagram_caption)
    return generator(caption, words)

def generate_funny_caption(caption, words):
    funny_templates = [
        f"When you're trying to be photogenic but end up with {caption} 😂 #PhotoFail #Relatable #Mood #Life",
        f"POV: You thought you looked good but the camera said '{caption}' 🤣 #Reality #Funny #Candid",
        f"That moment when {caption} and you can't even... 😅 #Awkward #Funny #Real #Moments",
        f"Me trying to be aesthetic: *gets {caption}* 🙃 #ExpectationVsReality #Funny #Relatable",
        f"When life gives you {caption}, make memes 🤪 #Funny #Life #Humor #Mood"
    ]
    return random.choice(funny_templates)

def generate_poetic_caption(caption, words):
    poetic_templates = [
        f"In whispered moments of grace, {caption} tells a story untold ✨ #Poetry #Beauty #Soul #Moment",
        f"Where light meets shadow, {caption} blooms eternal 🌸 #Poetic #Art #Beauty #Inspiration",
        f"Through the lens of wonder, {caption} speaks to hearts that listen 💫 #Poetry #Deep #Meaning #Art",
        f"Silent symphonies play where {caption} dances with time ⏰ #Poetic #Timeless #Beauty #Soul",
        f"In the cathedral of moments, {caption} becomes prayer 🙏 #Poetry #Spiritual #Beauty #Peace",
        f"Like verses written in light, {caption} captures eternity ∞ #Poetic #Eternal #Beauty #Art"
    ]
    return random.choice(poetic_templates)

def generate_aesthetic_caption(caption, words):
    aesthetic_templates = [
        f"soft mornings ☁️ {caption} #Aesthetic #Minimalist #Calm #Vibe #Clean",
        f"golden hour feelings when {caption} meets serenity ✨ #Aesthetic #Golden #Dreamy #Soft",
        f"finding beauty in {caption} 🤎 #Aesthetic #Simple #Pure #Minimalist #Vibe",
        f"quiet moments • {caption} • pure bliss ☁️ #Aesthetic #Quiet #Peace #Minimalist",
        f"captured: {caption} in all its gentle glory 🕊️ #Aesthetic #Gentle #Pure #Soft #Clean",
        f"when {caption} feels like a warm hug ☁️ #Aesthetic #Cozy #Soft #Warm #Minimalist"
    ]
    return random.choice(aesthetic_templates)

def generate_instagram_caption(caption, words):
    instagram_templates = [
        f"Living for moments like this! {caption} 💕 #InstaGood #Life #Happy #PhotoOfTheDay #Blessed",
        f"Caught in the perfect moment: {caption} 📸 #Instagram #Life #Moments #Memories #Good",
        f"This is what happiness looks like ➜ {caption} ✨ #InstaLife #Happiness #Vibes #Daily #Love",
        f"Making memories one photo at a time • {caption} 💫 #Memories #InstaGood #Life #Moments",
        f"Current mood: {caption} and loving it! 😍 #Mood #InstaDaily #Life #Happy #Blessed",
        f"Just me, my camera, and {caption} 📷 #Photography #InstaGood #Life #Capture #Moments"
    ]
    return random.choice(instagram_templates)

# === Fallback API styling (if available) ===
def try_api_styling(blip_caption, style):
    """Try API styling as enhancement, but don't depend on it"""
    if not USE_API or not HF_API_TOKEN:
        return None
    
    try:
        prompt = f"Rewrite this as a {style.lower()} social media caption: {blip_caption}"
        
        headers = {
            "Authorization": f"Bearer {HF_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Try a simple, reliable model
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            headers=headers,
            json={"inputs": prompt, "parameters": {"max_new_tokens": 80}},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "").strip()
    except:
        pass
    
    return None

# === Main logic ===
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="📷 Uploaded Image", use_container_width=True)
    
    with st.spinner("🧠 Analyzing image..."):
        blip_caption = generate_blip_caption(image)
    
    st.success("📝 Image Analysis:")
    st.markdown(f"> *{blip_caption}*")
    
    with st.spinner(f"✨ Creating {caption_style} caption..."):
        # Try API first (if available), then use advanced offline generation
        api_caption = try_api_styling(blip_caption, caption_style) if USE_API else None
        
        if api_caption and len(api_caption) > 20:
            styled_caption = api_caption
            st.info("🌐 Enhanced with AI styling")
        else:
            styled_caption = create_advanced_caption(blip_caption, caption_style)
            st.info("💡 Generated with advanced offline styling")
    
    st.success("🎉 Your Perfect Caption:")
    st.markdown(f"**{styled_caption}**")
    
    # Generate another option
    if st.button("🔄 Generate Another Caption"):
        styled_caption = create_advanced_caption(blip_caption, caption_style)
        st.markdown(f"**New Caption:** {styled_caption}")

