mport os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# DİKKAT: &amp; değil & kullanılmalı
GENELPARA_URL = "https://api.genelpara.com/json/?list=altin&sembol=GA,C,Y,T,XAUUSD"

def tg_send(text: str):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    r.raise_for_status()

def main():
    # 1) API çağrısı
    r = requests.get(GENELPARA_URL, timeout=20)
    r.raise_for_status()
    j = r.json()

    # 2) GenelPara yanıtı: { success, list, count, remaining, data: { ... } }
    data = j["data"]  # burada kesin "data" var (senin ekranda da var) [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)

    def pick(sym):
        item = data.get(sym, {})
        return item.get("alis"), item.get("satis")

    ga_a, ga_s = pick("GA")       # Gram
    c_a, c_s   = pick("C")        # Çeyrek
    y_a, y_s   = pick("Y")        # Yarım
    t_a, t_s   = pick("T")        # Tam
    o_a, o_s   = pick("XAUUSD")   # Ons

    # GitHub runner UTC olabilir → TR için +3
    now_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

    text = (
        "📌 GoldPrice Bot (API)\n"
        f"🕘 {now_tr} (TR)\n\n"
        f"🌍 ONS\n  Alış: {o_a} $ | Satış: {o_s} $\n\n"
        f"💰 GRAM\n  Alış: {ga_a} TL | Satış: {ga_s} TL\n\n"
        f"🪙 ÇEYREK\n  Alış: {c_a} TL | Satış: {c_s} TL\n\n"
        f"🪙 YARIM\n  Alış: {y_a} TL | Satış: {y_s} TL\n\n"
        f"🪙 TAM\n  Alış: {t_a} TL | Satış: {t_s} TL\n"
    )

    tg_send(text)

if _name_ == "_main_":
    try:
        main()
    except Exception as e:
        now_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")
        tg_send(f"⚠️ GoldPrice Bot\n🕘 {now_tr} (TR)\nHata: {e}")
        raise
