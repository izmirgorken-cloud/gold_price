import os
import requests
from datetime import datetime, timedelta

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# GenelPara API: altın verileri (GA,C,Y,T,XAUUSD) [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)
GENELPARA_URL = "https://api.genelpara.com/json/?list=altin&sembol=GA,C,Y,T,XAUUSD"

def now_tr() -> str:
    # GitHub runner çoğu zaman UTC; TR için +3
    return (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%Y %H:%M")

def tg_send(text: str) -> None:
    """
    Telegram Bot API sendMessage ile mesaj gönderir. [3](https://github.com/TelegramBots/Telegram.Bot)
    """
    if not TOKEN or not CHAT_ID:
        # Secretlar yoksa Telegram'a yazamayız; log'a bas
        print("ERROR: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")
        print(text)
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": CHAT_ID, "text": text}, timeout=20)
    # Telegram hata verirse loglayalım
    if r.status_code >= 400:
        print("Telegram HTTP", r.status_code, r.text)
    r.raise_for_status()

def pick(data: dict, sym: str):
    item = data.get(sym, {}) if isinstance(data, dict) else {}
    return item.get("alis"), item.get("satis")

def fmt(title: str, alis, satis, unit: str) -> str:
    a = alis if alis else "-"
    s = satis if satis else "-"
    return f"{title}\n  Alış: {a} {unit} | Satış: {s} {unit}"

def main():
    ts = now_tr()

    # 1) API çağrısı
    try:
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36",
    "Accept": "application/json,text/plain,/",
}
r = requests.get(GENELPARA_URL, headers=headers, timeout=20)
    except Exception as e:
        tg_send(f"⚠️ GoldPrice Bot\n🕘 {ts} (TR)\nGenelPara'ya istek atılamadı: {e}")
        return

    # 2) HTTP status kontrol
    if r.status_code != 200:
        preview = (r.text or "")[:300]
        tg_send(
            f"⚠️ GoldPrice Bot\n🕘 {ts} (TR)\n"
            f"GenelPara HTTP {r.status_code}\n"
            f"İlk 300 karakter:\n{preview}"
        )
        return

    # 3) JSON parse kontrol
    try:
        j = r.json()
    except Exception as e:
        preview = (r.text or "")[:300]
        tg_send(
            f"⚠️ GoldPrice Bot\n🕘 {ts} (TR)\n"
            f"JSON parse hatası: {e}\n"
            f"İlk 300 karakter:\n{preview}"
        )
        return

    # 4) Beklenen format: j['data'] içinde semboller bulunur [1](https://github.com/Mehmet020202/Hasalt-napi2026)[2](https://altin.in/)
    data = j.get("data")
    if not isinstance(data, dict):
        tg_send(
            f"⚠️ GoldPrice Bot\n🕘 {ts} (TR)\n"
            f"Beklenen 'data' alanı yok/uygunsuz.\n"
            f"Gelen anahtarlar: {list(j.keys()) if isinstance(j, dict) else 'unknown'}"
        )
        return

    # 5) Fiyatları çek
    ga_a, ga_s = pick(data, "GA")
    c_a, c_s   = pick(data, "C")
    y_a, y_s   = pick(data, "Y")
    t_a, t_s   = pick(data, "T")
    o_a, o_s   = pick(data, "XAUUSD")

    # 6) Mesaj formatla
    msg = "\n\n".join([
        f"📌 GoldPrice Bot (API)\n🕘 {ts} (TR)",
        fmt("🌍 ONS (XAUUSD)", o_a, o_s, "$"),
        fmt("💰 GRAM (GA)", ga_a, ga_s, "TL"),
        fmt("🪙 ÇEYREK (C)", c_a, c_s, "TL"),
        fmt("🪙 YARIM (Y)", y_a, y_s, "TL"),
        fmt("🪙 TAM (T)", t_a, t_s, "TL"),
    ])

    # 7) Telegram'a gönder
    tg_send(msg)

if __name__ == "__main__":
    main()
