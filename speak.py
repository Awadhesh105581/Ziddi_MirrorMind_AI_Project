from gtts import gTTS
import pygame
import time
import os

def speak(text):
    filename = "ziddi_voice.mp3"
    
    # 🎙️ Text to Speech
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    
    # 🔊 Play using pygame
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    # ⏳ Wait till speaking finishes
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # ✅ Stop and clean up
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # 🧹 Delete the voice file
    try:
        os.remove(filename)
    except Exception as e:
        print("⚠️ Can't delete file:", e)
