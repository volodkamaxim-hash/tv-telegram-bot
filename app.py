from flask import Flask, request
import requests
import threading
import time
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
RENDER_URL = "https://tv-telegram-bot-2vki.onrender.com"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def keep_alive():
    while True:
        time.sleep(600)
        try:
            requests.get(f"{RENDER_URL}/ping")
        except:
            pass

@app.route("/ping")
def ping():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data:
        symbol = data.get("symbol", "N/A")
        signal = data.get("signal", "N/A")
        timeframe = data.get("timeframe", "N/A")
        
        if signal == "UP":
            emoji = "🟢"
            direction = "ЛОНГ ▲"
        else:
            emoji = "🔴"
            direction = "ШОРТ ▼"
            
        msg = f"{emoji} {direction}\n📊 {symbol}\n⏱ Таймфрейм: {timeframe}м"
        send_telegram(msg)
    return "OK", 200

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
