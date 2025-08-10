# 🎙️ voice.py
# Handles speech input and output

import speech_recognition as sr
import pyttsx3
from config import LANGUAGE

engine = pyttsx3.init()

recognizer = sr.Recognizer()

def speak(text):
    print("🗣️ MirrorMind:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎧 Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language=LANGUAGE)
            return command
        except:
            return ""
