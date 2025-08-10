# 🧠 brain.py
# Combines prompt templates + memory

import json

MEMORY_FILE = "memory/ziddi_memory.json"

try:
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
except:
    memory = {}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def update_memory(key, value):
    memory[key] = value
    save_memory()

def get_memory():
    return memory


def build_prompt(user_input):
    with open("prompt_templates/ziddi_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()
    mem_str = "\n".join([f"{k}: {v}" for k, v in memory.items()])
    prompt = template.replace("{{memory}}", mem_str).replace("{{input}}", user_input)
    return prompt