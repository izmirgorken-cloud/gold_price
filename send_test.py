import os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def tg_send(text: str):
    # Telegram Bot API sendMessage [1](https://anlikaltinfiyatlari.com/altin/harem-altin)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    r.raise_for_status()

def main():
    # GitHub runner UTC; TR için +3
    ts_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

    # ŞİMDİLİK FIX / HARDCODE DEĞERLER
    prices = {
        "ONS":    {"alis": "5.110,20 $",  "satis": "5.114,60 $"},
        "GRAM":   {"alis": "7.245,61 ₺",  "satis": "7.388,91 ₺"},
        "CEYREK": {"alis": "11.877 ₺",    "satis": "12.048 ₺"},
        "YARIM":  {"alis": "23.739 ₺",    "satis": "24.110 ₺"},
        "TAM":    {"alis": "47.333 ₺",    "satis": "47.993 ₺"},
    }

    msg = (
        f"📌 GoldPrice Bot (FIX)\n"
        f"🕗 {ts_tr} (TR)\n\n"
        f"🌍 ONS\n  Alış: {prices['ONS']['alis']} | Satış: {prices['ONS']['satis']}\n\n"
        f"💰 GRAM\n  Alış: {prices['GRAM']['alis']} | Satış: {prices['GRAM']['satis']}\n\n"
        f"🪙 ÇEYREK\n  Alış: {prices['CEYREK']['alis']} | Satış: {prices['CEYREK']['satis']}\n\n"
        f"🪙 YARIM\n  Alış: {prices['YARIM']['alis']} | Satış: {prices['YARIM']['satis']}\n\n"
        f"🪙 TAM\n  Alış: {prices['TAM']['alis']} | Satış: {prices['TAM']['satis']}\n\n"
        "✅ Sistem stabil. API entegrasyonunu sonra açacağız."
    )

    tg_send(msg)

if _name_ == "_main_":
    main()
