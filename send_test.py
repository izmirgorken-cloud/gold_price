import os
import requests
from datetime import datetime

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# =========================
# ŞİMDİLİK HARDCODE DEĞERLER
# (RapidAPI gelince burası gerçek veriden dolacak)
# =========================
prices = {
    "ONS":    {"alis": "5.110,20 $",  "satis": "5.114,60 $"},
    "GRAM":   {"alis": "7.245,61 TL", "satis": "7.388,91 TL"},
    "CEYREK": {"alis": "11.877 TL",   "satis": "12.048 TL"},
    "YARIM":  {"alis": "23.739 TL",   "satis": "24.110 TL"},
    "TAM":    {"alis": "47.333 TL",   "satis": "47.993 TL"},
}

now_tr = datetime.now().strftime("%d.%m.%Y %H:%M")

text = (
    "📌 GoldPrice Bot (TEST)\n"
    f"🕘 {now_tr} (TR)\n\n"
    "🌍 ONS\n"
    f"  Alış: {prices['ONS']['alis']} | Satış: {prices['ONS']['satis']}\n\n"
    "💰 GRAM\n"
    f"  Alış: {prices['GRAM']['alis']} | Satış: {prices['GRAM']['satis']}\n\n"
    "🪙 ÇEYREK\n"
    f"  Alış: {prices['CEYREK']['alis']} | Satış: {prices['CEYREK']['satis']}\n\n"
    "🪙 YARIM\n"
    f"  Alış: {prices['YARIM']['alis']} | Satış: {prices['YARIM']['satis']}\n\n"
    "🪙 TAM\n"
    f"  Alış: {prices['TAM']['alis']} | Satış: {prices['TAM']['satis']}\n\n"
    "✅ Otomatik: GitHub Actions schedule ile gönderildi."
)

# Telegram Bot API - sendMessage [1](https://canlipiyasalar.romaaltin.com/)
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
resp = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
resp.raise_for_status()
print(resp.json())
