# server.py
import os
import asyncio
import threading
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# आपका bot logic import करो (अब भी वही generate_reply, build_prompt इस्तेमाल होगा)
from mirror import generate_reply
from brain import build_prompt

# TOKEN को environment variable से लो (Render में यही रखना है)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN env var")

app = Flask(__name__)

# --- Telegram Application बनाओ (अभी चलाओ मत) ---
telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Handlers (तुम्हारा मौजूदा logic यहाँ integrate)
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MirrorMind live है — बोलो, क्या सोचा?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    prompt = build_prompt(user_text)
    reply = generate_reply(prompt)
    await update.message.reply_text(reply)

telegram_app.add_handler(CommandHandler("start", start_command))
telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# --- एक अलग asyncio loop बनाओ और उसे background thread में चलाओ ---
loop = asyncio.new_event_loop()

def _run_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=_run_loop, daemon=True).start()

# --- इस loop पर application initialize और start करो ---
async def _init_and_start():
    await telegram_app.initialize()   # prepares bot & data
    # वैकल्पिक: Auto-set webhook if WEBHOOK_URL env var set
    webhook_url = os.environ.get("WEBHOOK_URL")  # set this after first deploy (see below)
    if webhook_url:
        await telegram_app.bot.set_webhook(webhook_url)
    await telegram_app.start()   # starts background tasks required by application

# schedule initialization on that loop
asyncio.run_coroutine_threadsafe(_init_and_start(), loop)

# --- Flask routes ---
@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    # Telegram will POST update JSON here
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    # schedule processing on the same asyncio loop (non-blocking)
    asyncio.run_coroutine_threadsafe(telegram_app.process_update(update), loop)
    return "", 200

# optional graceful shutdown - not required for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
