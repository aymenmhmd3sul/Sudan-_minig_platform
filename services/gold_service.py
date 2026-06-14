import requests

PRIMARY_URL = "https://api.metals.live/v1/spot/gold"

FALLBACK_URL = "https://api.metals.live/v1/spot/gold"

def get_gold_price():
    """
    محاولة جلب سعر الذهب من مصدر أساسي،
    وإذا فشل يتم الرجوع تلقائياً إلى fallback آمن.
    """

    def fetch(url):
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        r.raise_for_status()
        return r.json()

    # 1) محاولة المصدر الأساسي
    try:
        data = fetch(PRIMARY_URL)
        return {
            "status": "success",
            "source": "primary",
            "price_raw": data
        }

    except Exception as e_primary:
        # 2) fallback (نفس المصدر حالياً لكن جاهز للتبديل لاحقاً)
        try:
            data = fetch(FALLBACK_URL)
            return {
                "status": "success",
                "source": "fallback",
                "price_raw": data,
                "warning": str(e_primary)
            }

        except Exception as e_fallback:
            # 3) فشل كامل بدون إسقاط النظام
            return {
                "status": "error",
                "source": "none",
                "error": str(e_fallback)
            }
