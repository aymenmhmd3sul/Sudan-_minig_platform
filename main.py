from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"

def get_price():
    try:
        r = requests.get(BINANCE_URL, timeout=5)
        return float(r.json()["price"])
    except:
        return 2335.0


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/v1/gold-price")
def gold_price():
    return {"status": "success", "gold_usd": get_price()}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    price = get_price()

    return f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Sudan Mining Hub</title>

<style>
body {{
    margin:0;
    font-family: Arial;
    background:#0b1220;
    color:white;
}}

.container {{
    max-width:1100px;
    margin:auto;
    padding:15px;
}}

.header {{
    text-align:center;
    padding:20px;
    font-size:22px;
    font-weight:bold;
    background:#111827;
    border-radius:10px;
    margin-top:10px;
}}

.price {{
    text-align:center;
    font-size:48px;
    color:#22c55e;
    margin:20px 0;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
    gap:12px;
}}

.card {{
    background:#1f2937;
    padding:18px;
    border-radius:12px;
    text-align:center;
    transition:0.2s;
}}

.card:hover {{
    transform:scale(1.03);
    background:#273449;
}}

.footer {{
    text-align:center;
    margin-top:20px;
    padding:15px;
    color:#94a3b8;
    font-size:13px;
}}
</style>
</head>

<body>

<div class="container">

<div class="header">🟡 لوحة السودان للتعدين</div>

<div class="price">{price} USD</div>

<div class="grid">

<div class="card">📦 الطلبات</div>
<div class="card">👤 التجار</div>
<div class="card">⛏️ التعدين</div>
<div class="card">📢 الإعلانات</div>
<div class="card">💳 الاشتراك</div>

</div>

<div class="footer">منصة سودان للتعدين - نظام مباشر</div>

</div>

</body>
</html>
"""
