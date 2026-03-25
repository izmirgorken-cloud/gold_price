import os
import requests
from datetime import datetime, timezone, timedelta

# GoldAPI endpoint formatı: https://www.goldapi.io/api/{METAL}/{CURRENCY}
# Örn: https://www.goldapi.io/api/XAU/USD/20230617 ve header'da x-access-token ile key gönderimi örneklenmiş. [1](https://www.goldapi.io/)
GOLDAPI_URL = "https://www.goldapi.io/api/XAU/TRY"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOLDAPI_KEY = os.getenv("GOLDAPI_KEY")


def tr_now_str():
    tr_tz = timezone(timedelta(hours=3))  # TR = UTC+3
    return datetime.now(tr_tz).strftime("%d.%m.%Y %H:%M")


def goldapi_headers():
    # GoldAPI auth: header 'x-access-token: YOUR_API_KEY' [1](https://www.goldapi.io/)
    return {
        "x-access-token": GOLDAPI_KEY,
        "User-Agent": "GoldPriceBot/1.0 (GitHub Actions)",
        "Accept": "application/json",
    }


def fetch_gold():
    r = requests.get(GOLDAPI_URL, headers=goldapi_headers(), timeout=20)
    return r


def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    rt = requests.post(url, data=payload, timeout=20)
    rt.raise_for_status()


def main():
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID or not GOLDAPI_KEY:
        raise RuntimeError("Eksik env var: TELEGRAM_TOKEN / TELEGRAM_CHAT_ID / GOLDAPI_KEY")

    r = fetch_gold()

    if r.status_code != 200:
        preview = (r.text or "")[:300].replace("<", "&lt;").replace(">", "&gt;")
        msg = (
            f"⚠️ <b>GoldPrice Bot</b>\n"
            f"🕰 {tr_now_str()} (TR)\n"
            f"GoldAPI HTTP <b>{r.status_code}</b>\n"
            f"<b>İlk 300 karakter:</b>\n<code>{preview}</code>"
        )
        send_telegram(msg)
        return

    data = r.json()

    # GoldAPI örnek response alanları: timestamp, metal, currency, ask, bid, price, ch, chp, vb. [1](https://www.goldapi.io/)
    price = data.get("price")
    ask = data.get("ask")
    bid = data.get("bid")
    ch = data.get("ch")
    chp = data.get("chp")

    # Eğer dönerse opsiyonel gram/karat alanlarını da ekleyebiliriz.
    # Örnek response'ta price_gram_22K gibi alanlar gösteriliyor. [1](https://www.goldapi.io/)
    gram_24k = data.get("price_gram_24K")
    gram_22k = data.get("price_gram_22K")

    lines = [
        "✅ <b>GoldPrice Bot</b>",
        f"🕰 {tr_now_str()} (TR)",
        "💰 <b>XAU/TRY</b>",
        f"Price: <b>{price}</b>",
        f"Ask (Satış): <b>{ask}</b> | Bid (Alış): <b>{bid}</b>",
        f"Δ: <b>{ch}</b> ({chp}%)",
    ]

    # Opsiyonel alanlar varsa ekle
    if gram_24k is not None:
        lines.append(f"Gram 24K: <b>{gram_24k}</b>")
    if gram_22k is not None:
        lines.append(f"Gram 22K: <b>{gram_22k}</b>")

    send_telegram("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Son çare: hata bilgisini telegrama da basmaya çalış
        try:
            send_telegram(
                f"❌ <b>GoldPrice Bot Error</b>\n"
                f"🕰 {tr_now_str()} (TR)\n"
                f"<code>{str(e)[:350]}</code>"
            )
        except Exception:
            pass
        raise
