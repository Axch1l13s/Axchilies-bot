import requests
import re
import time
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

📊 Features
• 🔍 Auto Token Scanner
• 💰 Live Crypto Prices
• ⭐ Alpha Score
• 📈 Market Analysis
• ⚡ Real-Time Scanner

Paste any Solana Contract Address to start scanning.

💎 Stay Early. Stay Ahead."""
        )

    # ==========================
    # HELP
    # ==========================
    @bot.message_handler(commands=['help'])
    def help(message):
        bot.reply_to(
            message,
            """📚 Axchilies Alpha Scanner

Commands

🚀 /start
📖 /help
🏓 /ping
📊 /status
💰 /price <coin>
🚨 /newpairs

Examples

/price solana
/price bitcoin

Or simply paste any Solana Contract Address.

Example

So11111111111111111111111111111111111111112
"""
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
                    "Usage:\n/price solana\n/price bitcoin"
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

            bot.reply_to(
                message,
                f"""💰 {name} ({symbol})

Price
${price:,.4f}

24H Change
{change:.2f}%

Source
CoinGecko"""
            )

        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

    # ==========================
    # NEWPAIRS
    # ==========================
    @bot.message_handler(commands=['newpairs'])
    def newpairs(message):
        bot.reply_to(
            message,
            """🚧 New Pair Scanner

Coming Soon

• Live DexScreener Feed
• Pair Age Filter
• Liquidity Filter
• MarketCap Filter
• Telegram Alerts"""
        )

    # ==========================
    # AUTO SCAN
    # ==========================
    @bot.message_handler(func=lambda message: True)
    def auto_scan(message):

        contract = message.text.strip()

        # Cek apakah pesan adalah Solana Contract Address
        if not re.fullmatch(r"[1-9A-HJ-NP-Za-km-z]{32,44}", contract):
            return

        result = scan_token(contract)

        if result is None:
            bot.reply_to(message, "❌ Token not found.")
            return

        # ==========================
        # PAIR AGE
        # ==========================
        created = result.get("created", 0)

        if created:
            minutes = int((time.time() * 1000 - created) / 60000)

            if minutes < 60:
                pair_age = f"{minutes} Minutes"
            elif minutes < 1440:
                pair_age = f"{minutes // 60} Hours"
            else:
                pair_age = f"{minutes // 1440} Days"
        else:
            pair_age = "Unknown"
            minutes = 999999

        # ==========================
        # ALPHA SCORE
        # ==========================
        score = 50

        if result["liquidity"] >= 10000:
            score += 15

        if result["volume"] >= 50000:
            score += 15

        if result["marketcap"] >= 100000:
            score += 20

        if score >= 90:
            rating = "🟢 Excellent"
        elif score >= 75:
            rating = "🟢 Good"
        elif score >= 60:
            rating = "🟡 Moderate"
        else:
            rating = "🔴 High Risk"

        # ==========================
        # RISK ANALYSIS
        # ==========================
        warnings = []

        if result["liquidity"] < 5000:
            warnings.append("🔴 Very Low Liquidity")

        if result["marketcap"] < 25000:
            warnings.append("🟡 Very Low Market Cap")

        if minutes < 10:
            warnings.append("🟠 Very New Pair")

        if len(warnings) == 0:
            risk = "🟢 LOW"
        elif len(warnings) == 1:
            risk = "🟡 MEDIUM"
        else:
            risk = "🔴 HIGH"

        warning_text = "\n".join(warnings)

        if not warning_text:
            warning_text = "✅ No major warnings detected"

        # ==========================
        # SEND RESULT
        # ==========================
        text = f"""🚀 Axchilies Alpha Scanner

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🪙 Token
{result['name']} ({result[$'symbol']})

💵 Price : ${result['price']}
💰 Market Cap : ${result['marketcap']:,.0f}
💧 Liquidity : ${result['liquidity']:,.0f}
📈 Volume (24H) : ${result['volume']:,.0f}
🕒 Pair Age : {pair_age}
⭐ Alpha Score : {score}/100
📊 Rating : {rating}
⚠️ Risk : {risk}
🚨 Warnings : {warning_text}
🏦 DEX : {result['dex']}
⛓ Chain : {result['chain']}
🔗 Chart : {result['url']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Powered by Axchilies Alpha Scanner
"""

        bot.reply_to(message, text)