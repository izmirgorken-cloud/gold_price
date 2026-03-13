import os
import requests
from datetime import datetime, timedelta

# === Telegram Secrets (GitHub Secrets'tan geliyor) ===
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# === GenelPara API (Altın) ===
# GA: Gram, C: Çeyrek, Y: Yarım, T: Tam, XAUUSD: Ons [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)
GENELPARA_URL = "https://api.genelpara.com/json/?list=altin&sembol=GA,C,Y,T,XAUUSD"

def now_tr_str() -> str:
    # GitHub runner genelde UTC; TR için +3 saat
    return (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

def tg_send(text: str) -> None:
    """
    Telegram Bot API sendMessage ile mesaj gönderir. [3](https://github.com/TelegramBots/Telegram.Bot)
    Token / ChatID eksikse sadece log basar.
    """
    if not TOKEN or not CHAT_ID:
        print("ERROR: TELEGRAM_BOT_TOKEN veya TELEGRAM_CHAT_ID eksik (Secrets kontrol).")
        print("Mesaj:", text)
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)

    # Telegram hata döndürürse logla
    if r.status_code >= 400:
        print("Telegram HTTP Error:", r.status_code, r.text)

    r.raise_for_status()

def pick(data: dict, sym: str):
    """
    GenelPara 'data' objesinden sembolün alis/satis değerlerini çeker. [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)
    """
    item = data.get(sym, {}) if isinstance(data, dict) else {}
    return item.get("alis"), item.get("satis")

def format_pair(title: str, alis, satis, unit: str) -> str:
    a = alis if alis else "-"
    s = satis if satis else "-"
    return f"{title}\n  Alış: {a} {unit} | Satış: {s} {unit}"

def main() -> None:
    ts = now_tr_str()

    # 1) GenelPara API çağrısı
    r = requests.get(GENELPARA_URL, timeout=20)
    r.raise_for_status()

    # 2) JSON parse
    j = r.json()

    # 3) Beklenen format: j['data'] içinde GA,C,Y,T,XAUUSD var [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)
    data = j.get("data")
    if not isinstance(data, dict):
        # Beklenmedik cevap: Telegram'a bilgi ver
        keys = list(j.keys()) if isinstance(j, dict) else "unknown"
        tg_send(f"⚠️ GoldPrice Bot\n🕘 {ts} (TR)\nBeklenen 'data' alanı yok.\nAnahtarlar: {keys}")
        return

    ga_a, ga_s = pick(data, "GA")
    c_a, c_s   = pick(data, "C")
    y_a, y_s   = pick(data, "Y")
    t_a, t_s   = pick(data, "T")
    o_a, o_s   = pick(data, "XAUUSD")

    # 4) Mesaj formatı (senin istediğin gibi)
    msg = "\n\n".join([
        f"📌 GoldPrice Bot (API)\n🕘 {ts} (TR)",
        format_pair("🌍 ONS (XAUUSD)", o_a, o_s, "$"),
        format_pair("💰 GRAM (GA)", ga_a, ga_s, "TL"),
        format_pair("🪙 ÇEYREK (C)", c_a, c_s, "TL"),
        format_pair("🪙 YARIM (Y)", y_a, y_s, "TL"),
        format_pair("🪙 TAM (T)", t_a, t_s, "TL"),
    ])

    # 5) Telegram'a gönder
    tg_send(msg)

if _name_ == "_main_":
    try:
        main()
    except Exception as e:
        # Her türlü hatayı Telegram'a da bas
        ts = now_tr_str()
        tg_send(f"⚠️ GoldPrice Bot\n🕘 {ts} (TR)\nHata: {e}")
        raise
