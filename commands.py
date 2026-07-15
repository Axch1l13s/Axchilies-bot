
import requests

from telebot import TeleBot

def register_commands(bot: TeleBot):

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

    @bot.message_handler(commands=['help'])
    def help_command(message):
        bot.reply_to(
            message,
            """📚 Axchilies Alpha Scanner

Available Commands

🚀 /start
📖 /help
🏓 /ping
📊 /status

🚧 More features coming soon..."""
        )

    @bot.message_handler(commands=['ping'])
    def ping(message):
        bot.reply_to(message, "🏓 Pong!")

    @bot.message_handler(commands=['status'])
    def status(message):
@bot.message_handler(commands=['price'])
def price(message):
    try:
        args = message.text.split()

        if len(args) < 2:
            bot.reply_to(
                message,
                "Usage:\n/price sol\n/price btc\n/price eth"
            )
            return

        coin = args[1].lower()

        url = f"https://api.coingecko.com/api/v3/coins/{coin}"

        r = requests.get(url)

        if r.status_code != 200:
            bot.reply_to(message, "❌ Coin not found.")
            return

        data = r.json()

        name = data["name"]
        symbol = data["symbol"].upper()
        price = data["market_data"]["current_price"]["usd"]
        change = data["market_data"]["price_change_percentage_24h"]
        mc = data["market_data"]["market_cap"]["usd"]

        bot.reply_to(
            message,
            f"""💰 {name} ({symbol})

Price: ${price:,.2f}
24H: {change:.2f}%
Market Cap: ${mc:,.0f}

Source: CoinGecko"""
        )

    except Exception as e:
        bot.reply_to(message, f"Error: {e}")
        bot.reply_to(message, "🟢 Bot Status: Online")