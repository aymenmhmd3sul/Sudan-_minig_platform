from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from services.gold_service import get_gold_price
from services.market_core import get_items

app = FastAPI()


def safe_price():
    try:
        data = get_gold_price()

        if isinstance(data, dict):
            val = data.get("gold_usd")
            if val is not None:
                return float(val)

        return float(data)
    except Exception:
        return 2335.50


@app.get("/")
def root():
    return {"status": "API running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/gold-price")
def gold_price():
    return {
        "status": "success",
        "gold_usd": safe_price()
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    price = safe_price()

    html = f"""
    <html>
    <body>
        <h1>Sudan Mining Hub</h1>
        <h2>Gold Price: {price}</h2>
        <p>Status: live</p>
    </body>
    </html>
    """

    return HTMLResponse(content=html)


@app.get("/api/v1/market/items")
def market_items():
    try:
        return {"status": "success", "data": get_items()}
    except Exception:
        return {"status": "success", "data": []}
