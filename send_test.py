import os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# GenelPara: altın verisi (GA=Gram, C=Çeyrek, Y=Yarım, T=Tam, XAUUSD=Ons) [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)
GENELPARA_URL = "https://api.genelpara.com/json/?list=altin&sembol=GA,C,Y,T,XAUUSD"

def tg_send(text: str):
    # Telegram Bot API sendMessage [5](https://github.com/TelegramBots/Telegram.Bot)
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    r.raise_for_status()

def fmt(title, alis, satis, unit):
    a = alis if alis else "-"
    s = satis if satis else "-"
    return f"{title}\n  Alış: {a} {unit} | Satış: {s} {unit}"

def main():
    r = requests.get(GENELPARA_URL, timeout=20)
    r.raise_for_status()
    j = r.json()

    # Bazı yanıtlarda içerik "data" altında gelir. [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)
    data = j.get("data", j)

    def pick(sym):
        item = data.get(sym, {}) if isinstance(data, dict) else {}
        return item.get("alis"), item.get("satis")

    ga_a, ga_s = pick("GA")
    c_a,  c_s  = pick("C")
    y_a,  y_s  = pick("Y")
    t_a,  t_s  = pick("T")
    ons_a, ons_s = pick("XAUUSD")

    # GitHub runner UTC olabilir; TR saat göstermek için +3
    now_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

    text = (
        "📌 GoldPrice Bot\n"
        f"🕘 {now_tr} (TR)\n\n"
        + fmt("🌍 ONS", ons_a, ons_s, "$") + "\n\n"
        + fmt("💰 GRAM", ga_a, ga_s, "TL") + "\n\n"
        + fmt("🪙 ÇEYREK", c_a, c_s, "TL") + "\n\n"
        + fmt("🪙 YARIM", y_a, y_s, "TL") + "\n\n"
        + fmt("🪙 TAM", t_a, t_s, "TL")
    )

    tg_send(text)

if _name_ == "_main_":
    try:
        main()
    except Exception as e:
        now_tr = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")
        tg_send(f"⚠️ GoldPrice Bot\n🕘 {now_tr} (TR)\nAPI hatası: {e}")
