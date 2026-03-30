from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1487189296447225856/BVCvn7XsK45F7bsrS6EcVg1DFWhsum3Uacay9kBC602Jeq-E47lZnWX6B8F2ojktpzfv"
TELEGRAM_TOKEN = "8698506784:AAGU-p3F31S0oU8r1YIhAH6We0Wv9KlOuag"
CHAT_ID = "278863950"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json() or {}
    raw_msg = data.get('message', '🔔 Alerta')
    
    # Extrai dados reais do TradingView
    ticker = data.get('ticker', raw_msg.split()[0] if raw_msg.split() else 'N/A')
    exchange = data.get('exchange', 'N/A')
    interval = data.get('interval', 'N/A')
    close = data.get('close', 'N/A')
    
    # Mensagem BONITA
    message = f"🚨 *{ticker}* ({exchange})\n📊 *{interval}*\n💰 *R$ {close}*\n⏰ *{data.get('time', 'live')[:16]}*"
    
    # Telegram
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                params={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})
    
    # Discord
    requests.post(DISCORD_WEBHOOK, json={'content': message})
    
    return jsonify({"status": "OK"}), 200

@app.route('/', methods=['GET'])
def home():
    return "✅ LIVE!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
