from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# CONFIGS SUAS (já preenchidas)
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1487189296447225856/BVCvn7XsK45F7bsrS6EcVg1DFWhsum3Uacay9kBC602Jeq-E47lZnWX6B8F2ojktpzfv"
TELEGRAM_TOKEN = "8698506784:AAGU-p3F31S0oU8r1YIhAH6We0Wv9KlOuag"
CHAT_ID = "278863950"

@app.route('/', methods=['GET'])
def home():
    return "✅ TradingView Relay LIVE!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        message = data.get('message', '🔔 Alerta TradingView')
        
        # Telegram
        tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(tg_url, params={'chat_id': CHAT_ID, 'text': message})
        
        # Discord
        requests.post(DISCORD_WEBHOOK, json={'content': message})
        
        return jsonify({"status": "OK", "message": "Enviado para Telegram + Discord!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
