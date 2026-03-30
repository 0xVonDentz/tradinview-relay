from flask import Flask, request, jsonify
import requests
import os
import json

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1487189296447225856/BVCvn7XsK45F7bsrS6EcVg1DFWhsum3Uacay9kBC602Jeq-E47lZnWX6B8F2ojktpzfv"
TELEGRAM_TOKEN = "8698506784:AAGU-p3F31S0oU8r1YIhAH6We0Wv9KlOuag"
CHAT_ID = "278863950"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Aceita JSON ou texto puro
        if request.is_json:
            data = request.get_json()
        else:
            data = {'message': request.data.decode('utf-8')}
        
        # Extrai mensagem (funciona com qualquer payload)
        message = (data.get('message') or 
                  data.get('text', '') or 
                  data.get('description', '') or 
                  str(data) or 
                  '🔔 Alerta Watchlist')
        
        # TELEGRAM
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                    params={'chat_id': CHAT_ID, 'text': message})
        
        # DISCORD (embed simples)
        embed = {
            "embeds": [{
                "title": "🚨 TradingView Alert",
                "description": message,
                "color": 5763719
            }]
        }
        requests.post(DISCORD_WEBHOOK, json=embed)
        
        return jsonify({"status": "OK", "type": "watchlist_ok"}), 200
        
    except Exception as e:
        # Log erro mas continua funcionando
        print(f"Erro: {e}")
        return jsonify({"status": "OK"}), 200  # TradingView aceita

@app.route('/', methods=['GET'])
def home():
    return "✅ Watchlist + Individual LIVE!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
