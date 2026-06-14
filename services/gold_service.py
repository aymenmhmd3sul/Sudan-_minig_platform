import requests

def get_gold_price():
    price = None
    source = "fallback"

    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"
        r = requests.get(url, timeout=5)
        data = r.json()

        if "price" in data:
            price = float(data["price"])
            source = "binance"

    except Exception:
        pass

    # ضمان دائم: لا يوجد None إطلاقًا
    if price is None:
        price = 2335.50
        source = "system_fallback"

    return {
        "price": round(price, 2),
        "source": source
    }
