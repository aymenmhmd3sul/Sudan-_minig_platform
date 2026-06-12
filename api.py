from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

import models, database
from services.classification_service import classify_deal

app = FastAPI(title="Mining Smart API")

# ================= CORE =================

@app.get("/")
def root():
    return {"status": "API running Smart Version"}

@app.get("/prices")
def prices():
    return {
        "local": 114186,
        "global": 75.56,
        "status": "live"
    }

@app.get("/items")
def items():
    with Session(database.engine) as session:
        return session.query(models.TraderOffer).all()

# ================= REQUEST SYSTEM =================

class RequestIn(BaseModel):
    buyer_name: str
    whatsapp: str
    category: str
    specs: str
    images: Optional[List[str]] = []

@app.post("/request")
def create_request(data: RequestIn):
    with Session(database.engine) as session:

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

# ================= COMMISSION SYSTEM =================

class CommissionCalc(BaseModel):
    request_id: int

@app.post("/commission")
def commission(data: CommissionCalc):
    with Session(database.engine) as session:

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
