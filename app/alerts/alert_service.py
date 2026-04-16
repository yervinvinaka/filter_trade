import requests
import os

TELEGRAM_TOKEN = os.getenv("8635347002:AAHYH1Olc8BQFUPZOVdCPtaGMqpjpPmZWUk")
TELEGRAM_CHAT_ID = os.getenv("1357188939")

def send_alert(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("❌ Error Telegram:", response.text)
    else:
        print("📩 Mensaje enviado")