from flask import Flask
from threading import Thread
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Pump.fun monitor is alive!"

def keep_alive():
    def run():
        app.run(host='0.0.0.0', port=8080)
    t = Thread(target=run)
    t.start()

# ============ MONITOR CODE ============
import os

sent_tokens = set()
TG_TOKEN = '8041985955:AAGNPL_dWWWI5AWlYFue5NxkNOXsYqBOmiw'
TG_CHANNEL = '@PumpGuardians'

def fetch_trending_tokens():
    try:
        res = requests.get('https://pumpportal.fun/api/trending')
        if res.status_code == 200:
            return res.json()
        return []
    except Exception as e:
        print("Error fetching trending tokens:", e)
        return []

def format_token_message(token):
    return f"""🔥 <b>{token['name']} ({token['symbol']})</b>
    
Price: ${round(token['price'], 6)}
Market Cap: ${round(token['marketCap'], 2)}
24h Volume: ${round(token['volume'], 2)}
Position Change: {token['positionChange']}
Buy Link: https://pump.fun/{token['address']}
Chart: https://dexscreener.com/solana/{token['address']}
Contract: <code>{token['address']}</code>"""

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {
        "chat_id": TG_CHANNEL,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, data=data)
        print("Telegram message sent!" if r.status_code == 200 else f"Telegram failed: {r.text}")
    except Exception as e:
        print("Telegram error:", e)

def listen_and_send():
    print("Monitor started!")
    while True:
        tokens = fetch_trending_tokens()
        for token in tokens:
            token_id = token['address']
            if token_id not in sent_tokens:
                message = format_token_message(token)
                send_to_telegram(message)
                sent_tokens.add(token_id)
                print(f"Sent: {token['symbol']}")
        time.sleep(60)

# ============ START EVERYTHING ============
keep_alive()
listen_and_send()
