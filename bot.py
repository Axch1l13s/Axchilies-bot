import telebot
from config import BOT_TOKEN
from commands import register_commands

bot = telebot.TeleBot(BOT_TOKEN)

register_commands(bot)

print("🚀 Axchilies Alpha Scanner Running...")

bot.infinity_polling(skip_pending=True)