from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

@app.route("/")
def home():
    return "Bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    ticker = data.get("ticker","unknown")
    interval = data.get("interval","unknown")
    price = data.get("price","unknown")
    signal = data.get("signal","unknown")

    msg = f"{signal} | {ticker} | TF {interval} | Price {price}"

    send_message(msg)

    return "ok", 200
