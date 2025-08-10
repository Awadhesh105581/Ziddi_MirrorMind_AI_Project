from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from mirror import generate_reply
from brain import build_prompt
from config import TELEGRAM_BOT_TOKEN
import pytz

TIMEZONE = pytz.timezone("Asia/Kolkata")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("MirrorMind live है — बोलो, क्या सोचा?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    prompt = build_prompt(user_text)
    reply = generate_reply(prompt)
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Telegram MirrorMind Bot शुरू हो गया!")
    app.run_polling()

if __name__ == "__main__":
    main()
