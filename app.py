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
    
    # Se tem embeds, envia direto pro Discord
    if data.get('embeds'):
        requests.post(DISCORD_WEBHOOK, json=data)
        
        # Telegram recebe descrição
        msg = data['embeds'][0].get('description', 'Alerta TradingView')
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                    params={'chat_id': CHAT_ID, 'text': msg})
    else:
        # Fallback mensagem simples
        msg = data.get('message', '🔔 Alerta')
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                    params={'chat_id': CHAT_ID, 'text': msg})
        requests.post(DISCORD_WEBHOOK, json={'content': msg})
    
    return jsonify({"status": "OK"}), 200

@app.route('/', methods=['GET'])
def home():
    return "✅ EMBED Discord + Telegram LIVE!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
