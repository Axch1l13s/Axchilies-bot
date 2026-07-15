import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        """🚀 Welcome to Axchilies Alpha Scanner

Your AI-powered assistant for discovering early crypto opportunities.

📊 Features:
• 🚨 New Pair Alerts
• 🐋 Smart Money Tracking
• 🔍 Token Risk Analysis
• 📈 Market Monitoring
• ⚡ Real-Time Notifications

Type /help to view all available commands.

💎 Stay early. Stay ahead. Catch the next 100x."""
    )

print("Bot Running...")

bot.infinity_polling(skip_pending=True)

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(
        message,
        """📚 Axchilies Alpha Scanner

Available Commands:

🚀 /start - Start the bot
📖 /help - Show this help menu
🏓 /ping - Check if the bot is online
📊 /status - Bot status

🔜 Coming Soon:
🚨 /newpairs - New Solana Pair Alerts
🐋 /whales - Smart Money Tracker
🔍 /check - Token Risk Analysis
💰 /price - Live Token Prices

⚡ More features are coming soon!"""
    )
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.reply_to(message, "🏓 Pong! Bot is running successfully.")

@bot.message_handler(commands=['status'])
def status(message):
    bot.reply_to(
        message,
        """🟢 Bot Status

System: Online ✅
Server: Railway 🚂
Version: v1.0
Status: Running Smoothly 🚀"""
    )