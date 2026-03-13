import os
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

text = "✅ Test başarılı. GitHub Actions çalıştı ve Telegram'a mesaj gönderdi."

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
response = requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": text
    },
    timeout=20
)

response.raise_for_status()
print(response.json())
