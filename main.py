from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from services.gold_service import get_gold_price
from services.market_core import get_items, add_item

app = FastAPI(title="Sudan Mining Hub API")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/api/v1/gold-price")
def gold_price():
    try:
        return {"status": "success", "gold_usd": get_gold_price()}
    except:
        return {"status": "success", "gold_usd": 0}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    try:
        price_data = get_gold_price()
        price = price_data.get("price_raw", 0)
    except:
        price = 0

    return templates.TemplateResponse("index.html", {
        "request": request,
        "gold_price": price,
        "status": "live"
    })

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/market/items")
def market_items():
    return {"status": "success", "data": get_items()}
