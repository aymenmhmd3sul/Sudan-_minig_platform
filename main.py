from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price?symbol=PAXGUSDT"

def get_price():
    try:
        r = requests.get(BINANCE_URL, timeout=3)
        return float(r.json()["price"])
    except:
        return 2333.0


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    usd = get_price()
    local = usd * 600  # تقدير محلي (يمكن تغييره لاحقاً)

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
    padding:10px;
}}

.header {{
    text-align:center;
    padding:15px;
    background:#111827;
    border-radius:10px;
    font-size:20px;
    font-weight:bold;
}}

.ticker {{
    background:#0f172a;
    padding:10px;
    overflow:hidden;
    white-space:nowrap;
    border-bottom:1px solid #1f2937;
    margin-top:10px;
}}

.ticker span {{
    display:inline-block;
    padding-left:100%;
    animation: move 12s linear infinite;
}}

@keyframes move {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-100%); }}
}}

.price {{
    text-align:center;
    font-size:42px;
    color:#22c55e;
    margin:20px 0;
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
    gap:12px;
}}

.card {{
    background:#1f2937;
    padding:18px;
    border-radius:12px;
    text-align:center;
    cursor:pointer;
    transition:0.2s;
    font-size:14px;
}}

.card:hover {{
    transform:scale(1.05);
    background:#273449;
}}

.modal {{
    display:none;
    position:fixed;
    top:0;left:0;
    width:100%;height:100%;
    background:rgba(0,0,0,0.7);
}}

.modal-content {{
    background:#111827;
    margin:20% auto;
    padding:20px;
    width:85%;
    border-radius:12px;
    text-align:center;
}}

.close {{
    float:left;
    cursor:pointer;
    color:red;
    font-size:20px;
}}
</style>
</head>

<body>

<div class="container">

<div class="header">🟡 Sudan Mining Hub</div>

<div class="ticker">
<span>
💰 USD Gold: {usd:.2f} | 🇸🇩 Local: {local:.0f} SDG | 📈 Live Market Active
</span>
</div>

<div class="price">{usd:.2f} USD</div>

<div class="grid">

<div class="card" onclick="openModal('الطلبات')">📦 الطلبات</div>
<div class="card" onclick="openModal('التجار')">👤 التجار</div>
<div class="card" onclick="openModal('التعدين')">⛏️ التعدين</div>
<div class="card" onclick="openModal('الإعلانات')">📢 الإعلانات</div>
<div class="card" onclick="openModal('الاشتراك')">💳 الاشتراك</div>

</div>

</div>

<div class="modal" id="modal">
<div class="modal-content">
<span class="close" onclick="closeModal()">✖</span>
<h3 id="title"></h3>
<p>هذه نافذة تفاعلية قابلة للتطوير لاحقاً</p>
</div>
</div>

<script>
function openModal(title){{
    document.getElementById("title").innerText = title;
    document.getElementById("modal").style.display = "block";
}}

function closeModal(){{
    document.getElementById("modal").style.display = "none";
}}
</script>

</body>
</html>
"""
