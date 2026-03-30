from flask import Flask, request, jsonify
from datetime import datetime
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1487189296447225856/BVCvn7XsK45F7bsrS6EcVg1DFWhsum3Uacay9kBC602Jeq-E47lZnWX6B8F2ojktpzfv"
TELEGRAM_TOKEN = "8698506784:AAGU-p3F31S0oU8r1YIhAH6We0Wv9KlOuag"
CHAT_ID = "278863950"

def format_time(tv_time):
    """Converte {{time}} para dd/mm/yyyy HH:MM"""
    try:
        # Remove 'T' e 'Z' → 2026-03-30T09:45:00Z → 2026-03-30 09:45:00
        clean_time = tv_time.replace('T', ' ').replace('Z', '')
        dt = datetime.fromisoformat(clean_time)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return tv_time  # fallback

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        message = data.get('message', '🔔 Alerta TradingView')
        
        # Pega {{time}} da mensagem e formata
        if '{{time}}' in message:
            tv_time = data.get('time', datetime.now().isoformat())
            formatted_time = format_time(tv_time)
            message = message.replace('{{time}}', formatted_time)
        
        # TELEGRAM
        tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(tg_url, params={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'})
        
        # DISCORD
        requests.post(DISCORD_WEBHOOK, json={'content': message})
        
        return jsonify({"status": "OK", "time_formatted": formatted_time}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "LIVE!", "format": "dd/mm/yyyy HH:MM"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
