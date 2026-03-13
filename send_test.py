import os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# GenelPara API (Altın): GA,C,Y,T,XAUUSD
GENELPARA_URL = "https://api.genelpara.com/json/?list=altin&sembol=GA,C,Y,T,XAUUSD"

def tg_send(text: str):
    # Telegram Bot API sendMessage
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    r.raise_for_status()

def fmt(label, alis, satis, unit):
    a = alis if alis else "-"
    s = satis if satis else "-"
    return f"{label}\n  Alış: {a} {unit} | Satış: {s} {unit}"

def main():
    r = requests.get(GENELPARA_URL, timeout=20)
    r.raise_for_status()
    j = r.json()

    # Bazı yanıtlar "data" altında gelebilir
    data = j.get("data", j)

    def pick(sym):
        x = data.get(sym, {}) if isinstance(data, dict) else {}
        return x.get("alis"), x.get("satis")

    ga_a, ga_s   = pick("GA")
    c_a,  c_s    = pick("C")
    y_a,  y_s    = pick("Y")
    t_a,  t_s    = pick("T")
    ons_a, ons_s = pick("XAUUSD")

    # GitHub runner UTC; TR için +3
    ts_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

    msg = (
        f"📌 GoldPrice Bot\n🕗 {ts_tr} (TR)\n\n"
        + fmt("🌍 ONS (XAUUSD)", ons_a, ons_s, "$") + "\n\n"
        + fmt("💰 GRAM (GA)", ga_a, ga_s, "₺") + "\n\n"
        + fmt("🪙 ÇEYREK (C)", c_a, c_s, "₺") + "\n\n"
        + fmt("🪙 YARIM (Y)", y_a, y_s, "₺") + "\n\n"
        + fmt("🪙 TAM (T)", t_a, t_s, "₺")
    )

    tg_send(msg)

if _name_ == "_main_":
    try:
        main()
    except Exception as e:
        ts_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")
        tg_send(f"⚠️ GoldPrice Bot\n🕗 {ts_tr} (TR)\nGenelPara verisi çekilemedi: {e}")
