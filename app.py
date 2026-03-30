from flask import Flask, request
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1487189296447225856/BVCvn7XsK45F7bsrS6EcVg1DFWhsum3Uacay9kBC602Jeq-E47lZnWX6B8F2ojktpzfv"
TELEGRAM_TOKEN = "8698506784:AAGU-p3F31S0oU8r1YIhAH6We0Wv9KlOuag"
CHAT_ID = "278863950"

@app.route('/webhook', methods=['POST'])
def webhook():
    # SEMPRE aceita (Watchlist + Individual)
    raw = request.data.decode('utf-8', errors='ignore')
    
    # Monta mensagem
    if 'ticker' in raw:
        msg = f"🚨 Watchlist: {raw}"
    else:
        msg = raw or "🔔 Alert"
    
    # TELEGRAM
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                 data={'chat_id': CHAT_ID, 'text': msg})
    
    # DISCORD
    requests.post(DISCORD_WEBHOOK, json={'content': msg})
    
    return '', 200, {'Content-Type': 'text/plain'}  # TradingView aceita

@app.route('/', methods=['GET'])
def home():
    return "Watchlist OK"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
