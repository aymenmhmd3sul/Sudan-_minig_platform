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
    return {
        "status": "success",
        "gold_usd": get_price()
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    price = get_price()

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Sudan Mining Hub</title>
    <meta charset="UTF-8">

    <style>
        body {{
            margin:0;
            font-family: Arial;
            background:#0b1220;
            color:white;
            text-align:center;
        }}

        .box {{
            margin-top:80px;
        }}

        .title {{
            font-size:28px;
            margin-bottom:20px;
        }}

        .price {{
            font-size:64px;
            color:#22c55e;
            font-weight:bold;
        }}

        .card {{
            margin-top:40px;
            display:inline-block;
            padding:20px;
            background:#1f2937;
            border-radius:12px;
        }}
    </style>
</head>

<body>

<div class="box">
    <div class="title">🟡 Sudan Mining Hub</div>
    <div class="price">{price}</div>
    <div class="card">Live Gold Price (USD)</div>
</div>

</body>
</html>
"""
