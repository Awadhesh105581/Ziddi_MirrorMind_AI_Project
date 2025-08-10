# 🤖 telegram_bot.py
# Telegram bot integration

from telegram.ext import Updater, MessageHandler, Filters
from mirror import generate_reply
from brain import build_prompt
from config import TELEGRAM_BOT_TOKEN

def reply_handler(update, context):
    text = update.message.text
    prompt = build_prompt(text)
    reply = generate_reply(prompt)
    update.message.reply_text(reply)

def start_bot():
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))
    updater.start_polling()
    updater.idle()
