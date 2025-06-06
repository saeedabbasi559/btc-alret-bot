
from flask import Flask, request
import requests

app = Flask(__name__)

# اینجا توکن بات تلگرام رو بذار
TELEGRAM_TOKEN = 'توکن باتت اینجا'

# اینجا chat_id خودت یا گروهی که می‌خوای پیام بگیره
TELEGRAM_CHAT_ID = 'ایدی چتت اینجا'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    message = f"🚨 BTC Alert 🚨\n\n{data}"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)
    
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
