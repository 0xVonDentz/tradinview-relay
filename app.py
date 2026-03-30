from flask import Flask, request, jsonify
from datetime import datetime
import requests
import os
import json

app = Flask(__name__)

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1487189296447225856/BVCvn7XsK45F7bsrS6EcVg1DFWhsum3Uacay9kBC602Jeq-E47lZnWX6B8F2ojktpzfv"
TELEGRAM_TOKEN = "8698506784:AAGU-p3F31S0oU8r1YIhAH6We0Wv9KlOuag"
CHAT_ID = "278863950"

def format_time_br(time_str):
    """2026-03-30T13:52:00Z → 30/03/2026 13:52"""
    try:
        clean = time_str.replace('Z', '').replace('T', ' ')
        dt = datetime.fromisoformat(clean)
        return dt.strftime("%d/%m/%Y %H:%M")
    except:
        return time_str

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        
        # Extrai dados do TradingView
        ticker = data.get('ticker', 'N/A')
        exchange = data.get('exchange', 'N/A')
        interval = data.get('interval', 'N/A')
        close = data.get('close', 'N/A')
        volume = data.get('volume', 'N/A')
        tv_time = data.get('time') or data.get('timenow') or datetime.now().isoformat()
        
        # Formata hora
        formatted_time = format_time_br(tv_time)
        
        # Monta mensagem perfeita
        message = f"🚨 *{ticker}* ({exchange})\n📊 *{interval}*\n💰 *R$ {close}*\n⏰ *{formatted_time}*\n📈 *{volume}*"
        
        # ENVIA TELEGRAM (com Markdown)
        tg_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.get(tg_url, params={
            'chat_id': CHAT_ID, 
            'text': message, 
            'parse_mode': 'Markdown'
        })
        
        # ENVIA DISCORD
        requests.post(DISCORD_WEBHOOK, json={'content': message})
        
        return jsonify({
            "status": "OK", 
            "channels": ["Telegram", "Discord"],
            "time": formatted_time
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 200

@app.route('/', methods=['GET'])
def home():
    return "✅ Relay LIVE! dd/mm/yyyy HH:MM ✅"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
