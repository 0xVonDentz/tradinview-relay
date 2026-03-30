from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = "COLE_SUA_URL_DO_DISCORD_AQUI"
TELEGRAM_TOKEN = "COLE_SEU_TOKEN_AQUI"
CHAT_ID = "COLE_SEU_CHAT_ID_AQUI"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True) or {}
    ticker = data.get('ticker', 'N/A')
    exchange = data.get('exchange', 'N/A')
    interval = data.get('interval', 'N/A')
    close = data.get('close', 'N/A')
    time = data.get('time', 'N/A')
    volume = data.get('volume', 'N/A')

    message = f"🚨 {ticker} ({exchange})\n📊 {interval}\n💰 R$ {close}\n⏰ {time}\n📈 {volume}"

    requests.get(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": message},
        timeout=5
    )

    requests.post(
        DISCORD_WEBHOOK,
        json={"content": message},
        timeout=5
    )

    return jsonify({"status": "OK"}), 200

@app.route('/')
def home():
    return "LIVE"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
