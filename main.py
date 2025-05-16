import requests
import time
import threading
from flask import Flask
from datetime import datetime

# Telegram Bot Settings
BOT_TOKEN = '8041985955:AAGNPL_dWWWI5AWlYFue5NxkNOXsYqBOmiw'
CHANNEL_USERNAME = '@PumpGuardians'

# ذخیره شناسه‌های توکن برای جلوگیری از ارسال تکراری
sent_tokens = set()

# Keep-alive server using Flask
app = Flask('')

@app.route('/')
def home():
    return "I'm alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

# ارسال پیام به تلگرام
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHANNEL_USERNAME,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': False
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram Error:", e)

# فرمت پیام توکن
def format_token(token):
    name = token.get("tokenName", "Unknown")
    symbol = token.get("tokenSymbol", "")
    mint = token.get("tokenId", "")
    twitter = token.get("twitter", "")
    website = token.get("website", "")
    price = round(token.get("price", 0), 8)
    mc = int(token.get("marketCap", 0))
    holders = token.get("holders", 0)
    age = round(token.get("ageInSeconds", 0) / 60, 1)
    dev = token.get("creatorAccount", "")

    msg = f"""<b>🔥 Trending on Pump.fun</b>

<b>Name:</b> {name} ({symbol})
<b>Price:</b> ${price}
<b>Market Cap:</b> ${mc}
<b>Holders:</b> {holders}
<b>Age:</b> {age} mins

<b>🧠 Dev Wallet:</b> <code>{dev}</code>

🔗 <b>Buy:</b> https://pump.fun/{mint}
📊 <b>Chart:</b> https://birdeye.so/token/{mint}
{f'🐦 <b>Twitter:</b> {twitter}' if twitter else ''}
{f'🌐 <b>Website:</b> {website}' if website else ''}

#PumpFun #Solana #MemeCoin
"""
    return msg

# اجرای مانیتورینگ
def monitor_trending_tokens():
    while True:
        try:
            res = requests.get("https://pump.fun/api/trending")
            if res.status_code == 200:
                tokens = res.json()
                for token in tokens:
                    mint = token.get("tokenId")
                    if mint and mint not in sent_tokens:
                        sent_tokens.add(mint)
                        msg = format_token(token)
                        send_telegram_message(msg)
                        time.sleep(2)  # جلوگیری از محدودیت تلگرام
        except Exception as e:
            print("Error fetching trending tokens:", e)
        time.sleep(60)  # هر ۶۰ ثانیه بررسی مجدد

# اجرای نهایی
keep_alive()
monitor_trending_tokens()