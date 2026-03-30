from flask import Flask, request, jsonify
from datetime import datetime
import re
import requests
import os

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1487189296447225856/BVCvn7XsK45F7bsrS6EcVg1DFWhsum3Uacay9kBC602Jeq-E47lZnWX6B8F2ojktpzfv"
TELEGRAM_TOKEN = "8698506784:AAGU-p3F31S0oU8r1YIhAH6We0Wv9KlOuag"
CHAT_ID = "278863950"

def format_brazilian_time(time_str):
    """2026-03-30T13:52:00Z → 30/03/2026 13:52"""
    try:
        # Remove Z e converte
        clean = time_str.replace('Z', '').replace('T', ' ')
        dt = datetime.fromisoformat(clean)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return time_str

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        raw_message = data.get('message', '🔔 Alerta')
        
        # Pega {{time}} dos dados do TradingView
        tv_time = data.get('time', '') or data.get('timenow', '')
        if tv_time:
            formatted_time = format_brazilian_time(tv_time)
            raw_message = raw_message.replace('{{time}}', formatted_time)
        
        # Envia mensagens formatadas
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", 
                    params={'chat_id': CHAT_ID, 'text': raw_message, 'parse_mode': 'Markdown'})
        
        requests.post(DISCORD_WEBHOOK, json={'content': raw_message})
        
        return jsonify({"status": "OK", "formatted_time": formatted_time}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/', methods=['GET'])
def home():
    return "✅ Relay LIVE! Formato: dd/mm/yyyy HH:MM"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
