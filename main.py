from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.gold_service import get_gold_price
from services.market_core import get_items

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    return {"status": "API running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/gold-price")
def gold_price():
    price_data = get_gold_price()
    return {
        "status": "success",
        "gold_usd": float(price_data.get("gold_usd", 0))
    }

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    price_data = get_gold_price()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "gold_price": price_data,
        "status": "live"
    })

@app.get("/api/v1/market/items")
def market_items():
    try:
        return {"status": "success", "data": get_items()}
    except Exception:
        return {"status": "success", "data": []}
