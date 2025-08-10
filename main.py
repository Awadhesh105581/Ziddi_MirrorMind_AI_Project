# 🚀 main.py
# Entry point for voice-based MirrorMind

from voice import listen, speak
from mirror import generate_reply
from brain import build_prompt, update_memory
from speak import speak

speak("मैं ज़िद्दी MirrorMind हूं, बताओ क्या सोच रहे हो?")

while True:
    query = listen()
    if query.lower() in ["exit", "बंद हो जाओ", "stop"]:
        speak("ठीक है दोस्त, फिर मिलेंगे।")
        break
    prompt = build_prompt(query)
    response = generate_reply(prompt)
    speak(response)
    update_memory("last_topic", query)
    print("🧠 MirrorMind:", response)  
