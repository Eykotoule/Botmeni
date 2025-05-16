import requests
import time
import telegram
from keep_alive import keep_alive

TELEGRAM_BOT_TOKEN = '8041985955:AAGNPL_dWWWI5AWlYFue5NxkNOXsYqBOmiw'
CHANNEL_USERNAME = '@PumpGuardians'

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def fetch_trending_tokens():
    url = "https://pumpportal.fun/api/trending"
    try:
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print("Error fetching data:", e)
        return []

def format_message(token):
    price = token.get("price", "N/A")
    mc = token.get("market_cap", "N/A")
    name = token.get("name", "N/A")
    symbol = token.get("symbol", "")
    twitter = token.get("twitter", "")
    website = token.get("website", "")
    address = token.get("address", "")
    dev = token.get("dev", "")
    holders = token.get("holders", "N/A")
    chart = f"https://pump.fun/{address}"
    solscan = f"https://solscan.io/token/{address}"
    buy = f"https://pump.fun/{address}"

    msg = f"""
🔥 #{symbol.upper()} - *{name}* is trending!

• Price: ${price}
• Market Cap: ${mc}
• Holders: {holders}
• Dev Wallet: [{dev[:4]}...{dev[-4:]}](https://solscan.io/account/{dev})
• Contract: `{address}`

🌐 [Website]({website}) | [Twitter]({twitter})
📈 [Chart]({chart}) | [Buy Now]({buy}) | [Solscan]({solscan})
"""
    return msg

def send_to_telegram():
    tokens = fetch_trending_tokens()
    for token in tokens:
        try:
            message = format_message(token)
            bot.send_message(chat_id=CHANNEL_USERNAME, text=message, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)
            time.sleep(1)  # جلوگیری از اسپم شدن
        except Exception as e:
            print("Error sending message:", e)

keep_alive()

while True:
    send_to_telegram()
    time.sleep(3600)  # اجرا هر یک ساعت
