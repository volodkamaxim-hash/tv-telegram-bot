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
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})

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
        price = data.get("price", "N/A")

        # Эмодзи для сигнала
        if signal == "UP":
            signal_emoji = "🟢"
            direction = "ЛОНГ ▲"
        elif signal == "DOWN":
            signal_emoji = "🔴"
            direction = "ШОРТ ▼"
        elif signal == "ТЕСТ СОПРОТИВЛЕНИЯ":
            signal_emoji = "⚠️"
            direction = "ТЕСТ СОПРОТИВЛЕНИЯ 🔴"
        elif signal == "ТЕСТ ПОДДЕРЖКИ":
            signal_emoji = "⚠️"
            direction = "ТЕСТ ПОДДЕРЖКИ 🟢"
        else:
            signal_emoji = "📌"
            direction = signal

        # Эмодзи для таймфрейма
        tf = str(timeframe)
        if tf == "60":
            tf_emoji = "🚨🚨 ЧАСОВИК 🚨🚨"
        elif tf == "240":
            tf_emoji = "🚨🚨🚨🚨🚨🚨 4 ЧАСА 🚨🚨🚨🚨🚨🚨"
        elif tf == "15":
            tf_emoji = "15м"
        elif tf == "30":
            tf_emoji = "30м"
        elif tf == "5":
            tf_emoji = "5м"
        else:
            tf_emoji = f"{tf}м"

        msg = (
            f"{signal_emoji} <b>{direction}</b>\n"
            f"📊 {symbol}\n"
            f"⏱ {tf_emoji}\n"
            f"💰 Цена: <b>{price}</b>"
        )
        send_telegram(msg)
    return "OK", 200

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
