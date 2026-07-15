import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🔥 Axchilies Alpha Bot Online!\n\nSelamat datang bang 😎"
    )

print("Bot Running...")

bot.infinity_polling(skip_pending=True)