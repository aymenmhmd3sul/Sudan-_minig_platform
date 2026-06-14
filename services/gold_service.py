import requests

API_URL = "https://api.metals.live/v1/spot/gold"

def get_gold_price():
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, list) and data:
            price = data[0][1]
        else:
            return {"error": "bad format"}

        return {"gold_price_usd": price, "currency": "USD"}

    except Exception as e:
        return {"error": str(e)}
