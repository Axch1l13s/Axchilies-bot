import requests
import re
import time
from telebot import TeleBot
from scanner import scan_token
from security import check_security


def safe_float(value):
    try:
        return float(value or 0)
    except:
        return 0


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

Example:

/price solana

Or paste Solana Contract Address."""
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
                bot.reply_to(message, "Usage: /price solana")
                return

            coin = args[1].lower()

            url = f"https://api.coingecko.com/api/v3/coins/{coin}"

            r = requests.get(url, timeout=10)

            if r.status_code != 200:
                bot.reply_to(message, "❌ Coin not found")
                return

            data = r.json()

            current = data["market_data"]["current_price"]["usd"]
            change = data["market_data"]["price_change_percentage_24h"]

            bot.reply_to(
                message,
                f"""💰 {data['name']} ({data['symbol'].upper()})

Price:
${current}

24H:
{change:.2f}%

Source:
CoinGecko"""
            )

        except Exception as e:
            print("PRICE ERROR:", e)
            bot.reply_to(message, "❌ Price service error")


    # ==========================
    # NEW PAIRS
    # ==========================
    @bot.message_handler(commands=['newpairs'])
    def newpairs(message):

        bot.reply_to(
            message,
            """🚧 New Pair Scanner

Coming Soon

• DexScreener Feed
• Liquidity Filter
• Market Cap Filter
• Smart Money Tracking"""
        )


    # ==========================
    # AUTO SCAN
    # ==========================
    @bot.message_handler(func=lambda message: message.content_type == "text")
    def auto_scan(message):

        try:

            contract = message.text.strip()

            if not re.fullmatch(
                r"[1-9A-HJ-NP-Za-km-z]{32,44}",
                contract
            ):
                return


            result = scan_token(contract)

            if not result:
                bot.reply_to(
                    message,
                    "❌ Token data not found"
                )
                return


            # SECURITY SAFE
            try:
                security = check_security(contract) or {}
            except Exception as e:
                print("SECURITY ERROR:", e)
                security = {}


            # DATA SAFE

            marketcap = safe_float(
                result.get("marketcap")
            )

            liquidity = safe_float(
                result.get("liquidity")
            )

            volume = safe_float(
                result.get("volume")
            )


            # ==========================
            # PAIR AGE
            # ==========================

            created = result.get("created",0)

            minutes = 999999
            pair_age = "Unknown"

            if created:

                minutes = int(
                    (time.time()*1000 - created) / 60000
                )

                if minutes < 60:
                    pair_age=f"{minutes} Minutes"

                elif minutes < 1440:
                    pair_age=f"{minutes//60} Hours"

                else:
                    pair_age=f"{minutes//1440} Days"


            # ==========================
            # SCORE
            # ==========================

            score = 50

            if liquidity >= 10000:
                score +=15

            if volume >=50000:
                score +=15

            if marketcap >=100000:
                score +=20


            if score >=90:
                rating="🟢 Excellent"

            elif score>=75:
                rating="🟢 Good"

            elif score>=60:
                rating="🟡 Moderate"

            else:
                rating="🔴 Risk"


            # ==========================
            # WARNING
            # ==========================

            warnings=[]

            if liquidity <5000:
                warnings.append(
                    "🔴 Low Liquidity"
                )

            if marketcap <25000:
                warnings.append(
                    "🟡 Low Market Cap"
                )

            if minutes <10:
                warnings.append(
                    "🟠 New Pair"
                )


            warning_text="\n".join(warnings)

            if not warning_text:
                warning_text="✅ No major warning"


            # ==========================
            # RESULT
            # ==========================

            text=f"""🚀 Axchilies Alpha Scanner

━━━━━━━━━━━━━━

🪙 Token
{result.get('name','Unknown')} ({result.get('symbol','N/A')})

💵 Price:
${result.get('price',0)}

💰 Market Cap:
${marketcap:,.0f}

💧 Liquidity:
${liquidity:,.0f}

📈 Volume:
${volume:,.0f}

🕒 Pair Age:
{pair_age}

⭐ Alpha Score:
{score}/100

📊 Rating:
{rating}

🛡 Security:
Mint:
{security.get('mint_authority','Unknown')}

Freeze:
{security.get('freeze_authority','Unknown')}

Risk:
{security.get('risk','Unknown')}

🚨 Warning:
{warning_text}

🏦 DEX:
{result.get('dex','Unknown')}

🔗 Chart:
{result.get('url','N/A')}

━━━━━━━━━━━━━━
⚡ Axchilies Alpha Scanner
"""


           