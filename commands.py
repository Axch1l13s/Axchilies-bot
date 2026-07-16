import requests
import re
from telebot import TeleBot
from scanner import scan_token


def register_commands(bot: TeleBot):

    # ==========================
    # START
    # ==========================
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(
            message,
            """🚀 Welcome to Axchilies Alpha Scanner

Your AI-powered assistant for discovering early crypto opportunities.

📊 Features:
• 🚨 New Pair Alerts
• 🔍 Token Scanner
• 💰 Live Crypto Prices
• 📈 Market Monitoring
• ⚡ Real-Time Notifications

Type /help to view all available commands.

💎 Stay early. Stay ahead. Catch the next 100x."""
        )

    # ==========================
    # HELP
    # ==========================
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
💰 /price <coin>
🔍 /scan <contract>
🚨 /newpairs

Examples

/price solana
/price bitcoin

/scan So11111111111111111111111111111111111111112

🚀 More features coming soon..."""
        )

    # ==========================
    # PING
    # ==========================
    @bot.message_handler(commands=['ping'])
    def ping(message):
        bot.reply_to(message, "🏓 Pong!")

    # ==========================
    # STATUS
    # ==========================
    @bot.message_handler(commands=['status'])
    def status(message):
        bot.reply_to(message, "🟢 Bot Status: Online")

    # ==========================
    # PRICE
    # ==========================
    @bot.message_handler(commands=['price'])
    def price(message):
        try:
            args = message.text.split()

            if len(args) < 2:
                bot.reply_to(
                    message,
                    "Usage:\n/price solana\n/price bitcoin\n/price ethereum"
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
            price_usd = data["market_data"]["current_price"]["usd"]
            change = data["market_data"]["price_change_percentage_24h"]

            text = (
                f"💰 {name} ({symbol})\n\n"
                f"Price: ${price_usd:,.2f}\n"
                f"24H Change: {change:.2f}%\n\n"
                f"Source: CoinGecko"
            )

            bot.reply_to(message, text)

        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

    # ==========================
    # NEW PAIRS
    # ==========================
    @bot.message_handler(commands=['newpairs'])
    def newpairs(message):
        bot.reply_to(
            message,
            """🚧 New Pair Scanner

This feature is currently under development.

Next update:
• 🚨 Live DexScreener Scanner
• 💧 Liquidity Filter
• 💰 Market Cap Filter
• ⏱ Pair Age Filter
• 📲 Telegram Alerts

Stay tuned! 🚀"""
        )

    # ==========================
    # SCAN
    # ==========================
    @bot.message_handler(commands=['scan'])
    def scan(message):

        args = message.text.split()

        if len(args) < 2:
            bot.reply_to(
                message,
                """Usage:

/scan <contract_address>

Example:

/scan So11111111111111111111111111111111111111112"""
            )
            return

        contract = args[1]

        result = scan_token(contract)

        if result is None:
            bot.reply_to(message, "❌ Token not found.")
            return

        text = f"""🔍 Token Analysis

🪙 Token: {result['name']} ({result['symbol']})

💵 Price: ${result['price']}
💧 Liquidity: ${result['liquidity']:,.0f}
📈 Volume (24H): ${result['volume']:,.0f}

🏦 DEX: {result['dex']}
⛓ Chain: {result['chain']}

🔗 Chart:
{result['url']}
"""

        bot.reply_to(message, text)

    @bot.message_handler(func=lambda message: True)
def auto_scan(message):

    text = message.text.strip()

    # Deteksi contract Solana (panjang sekitar 32-44 karakter)
    if re.fullmatch(r"[1-9A-HJ-NP-Za-km-z]{32,44}", text):

        result = scan_token(text)

        if result is None:
            bot.reply_to(message, "❌ Token not found.")
            return

        reply = f"""🔍 Token Analysis

🪙 Token: {result['name']} ({result['symbol']})

💵 Price: ${result['price']}
💧 Liquidity: ${result['liquidity']:,.0f}
📈 Volume (24H): ${result['volume']:,.0f}

🏦 DEX: {result['dex']}
⛓ Chain: {result['chain']}

🔗 Chart:
{result['url']}
"""

        bot.reply_to(message, reply)