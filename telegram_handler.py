# 📁 FaizanCloudTrap/telegram_handler.py
import requests

BOT_TOKEN = "7901711799:AAEWnySjRO5KgEMpUQmz7fwnYzlumt_AlX4"
CHAT_ID = "6908281054"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)
