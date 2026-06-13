from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlmodel import SQLModel, select
from typing import List, Optional

import models
from database import engine
from services.classification_service import classify_deal

app = FastAPI(title="Sudan Mining Hub API", version="1.0")

# ================= ROOT =================
@app.get("/")
def root():
    return {"status": "running"}

# ================= PRICES =================
@app.get("/api/v1/prices")
def get_prices():
    return {
        "local_price": 114842,
        "global_price": 75.56,
        "direction": "مستقر",
        "change": 0,
        "history": [114700, 114750, 114800, 114850]
    }

# ================= MARKET =================
@app.get("/api/v1/market/items")
def get_items():
    try:
        with Session(engine) as session:
            items = session.query(models.MarketItem).all()

            return [
                {
                    "id": x.id,
                    "request_id": x.request_id,
                    "trader_id": x.trader_id,
                    "price": x.price,
                    "details": x.details,
                    "status": x.status
                }
                for x in items
            ]

    except Exception as e:
        return {"error": str(e)}

# ================= REQUEST =================
class RequestIn(BaseModel):
    buyer_name: str
    whatsapp: str
    category: str
    specs: str
    images: Optional[List[str]] = []

@app.post("/api/v1/request")
def create_request(data: RequestIn):
    with Session(engine) as session:

        req = models.BuyerRequest(
            buyer_name=data.buyer_name,
            whatsapp=data.whatsapp,
            category=data.category,
            specs=data.specs
        )

        req.is_heavy_deal = classify_deal(data.category, data.specs)
        req.estimated_value = "500000" if req.is_heavy_deal else "100000"

        session.add(req)
        session.commit()
        session.refresh(req)

        return {
            "status": "created",
            "id": req.id,
            "is_heavy_deal": req.is_heavy_deal,
            "estimated_value": req.estimated_value,
            "images": data.images
        }

# ================= COMMISSION =================
class CommissionCalc(BaseModel):
    request_id: int

@app.post("/api/v1/commission")
def commission(data: CommissionCalc):
    with Session(engine) as session:

        req = session.get(models.BuyerRequest, data.request_id)

        if not req:
            return {"error": "not found"}

        commission_value = "0.25%" if req.is_heavy_deal else "100000"

        return {
            "request_id": req.id,
            "status": req.status,
            "commission": commission_value,
            "confirmed": True
        }
