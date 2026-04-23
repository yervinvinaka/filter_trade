import requests
from app.core.config import settings


def send_alert(message: str):
    if not settings.TELEGRAM_TOKEN or not settings.TELEGRAM_CHAT_ID:
        print("❌ Telegram no configurado")
        return

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print("❌ Error Telegram:", response.text)
        else:
            print("📩 Alerta enviada")

    except Exception as e:
        print("❌ Error enviando alerta:", e)