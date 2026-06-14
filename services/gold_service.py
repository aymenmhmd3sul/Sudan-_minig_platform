import requests

URL = "https://api.metals.live/v1/spot/gold"

def get_gold_price():
    try:
        response = requests.get(
            URL,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        data = response.json()

        return {
            "price_raw": data,
            "status": "success"
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
