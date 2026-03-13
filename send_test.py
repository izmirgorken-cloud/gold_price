import os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# GenelPara: GA,C,Y,T,XAUUSD sembolleri (Gram, Çeyrek, Yarım, Tam, Ons) [3](https://www.youtube.com/watch?v=bcGwZHmjiyU)[4](https://chatarmin.com/en/blog/whats-app-api-send-messages)
GENELPARA_URL = "https://api.genelpara.com/json/?list=altin&sembol=GA,C,Y,T,XAUUSD"

def tg_send(text: str):
    # Telegram Bot API sendMessage [5](https://anlikaltinfiyatlari.com/altin/harem-altin)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    r.raise_for_status()

def fmt(label, alis, satis, unit):
    a = alis if alis else "-"
    s = satis if satis else "-"
    return f"{label}\n  Alış: {a} {unit} | Satış: {s} {unit}"

def main():
    try:
        r = requests.get(GENELPARA_URL, timeout=20)
        r.raise_for_status()
        j = r.json()

        # Bazı cevaplarda asıl içerik "data" altında geliyor. [3](https://www.youtube.com/watch?v=bcGwZHmjiyU)[4](https://chatarmin.com/en/blog/whats-app-api-send-messages)
        data = j.get("data", j)

        def pick(sym):
            x = data.get(sym, {}) if isinstance(data, dict) else {}
            return x.get("alis"), x.get("satis")

        ga_a, ga_s     = pick("GA")
        c_a,  c_s      = pick("C")
        y_a,  y_s      = pick("Y")
        t_a,  t_s      = pick("T")
        ons_a, ons_s   = pick("XAUUSD")

        # GitHub runner UTC olur; TR göstermek için +3 saat ekliyoruz
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

    except Exception as e:
        ts_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")
        tg_send(f"⚠️ GoldPrice Bot\n🕗 {ts_tr} (TR)\nGenelPara verisi çekilemedi: {e}")

if _name_ == "_main_":
    main()
``
