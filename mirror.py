# 🧠 mirror.py
# Handles Gemini-based response generation

import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')


def generate_reply(prompt):
    response = model.generate_content(prompt)
    
    # Check if response has parts
    if response.candidates and response.candidates[0].content.parts:
        return response.text
    else:
        return "⚠️ माफ़ करना, मैं इस पर कोई जवाब नहीं दे पाया। ज़रा दोबारा पूछो ज़रा ज़िद्दी अंदाज़ में।"
