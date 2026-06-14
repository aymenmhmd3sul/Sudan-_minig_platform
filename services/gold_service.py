import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_gold_price():
    return {
        "status": "success",
        "source": "stable_core",
        "price_raw": 2335.50
    }
