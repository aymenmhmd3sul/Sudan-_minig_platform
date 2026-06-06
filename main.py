from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_session
# تحديث الاستيراد ليشمل الجداول الجديدة والقديمة معاً
from models import (
    MiningSite, Equipment, Production, GoldPrice, Report, 
    EquipmentOrder, MerchantBid
)

app = FastAPI(title="Sudan Mining Hub API", version="1.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # سيقوم تلقائياً بإنشاء الجداول الجديدة في PostgreSQL دون التأثير على الجداول الحالية
    SQLModel.metadata.create_all(engine)

@app.get("/")
def root():
    return {"status": "running", "database": "PostgreSQL Connected"}

# --- [1] عمليات مواقع التعدين (Mining Sites CRUD) ---
@app.get("/api/v1/sites", response_model=List[MiningSite])
def read_sites(session: Session = Depends(get_session)):
    return session.exec(select(MiningSite)).all()

@app.post("/api/v1/sites", response_model=MiningSite, status_code=201)
def create_site(site: MiningSite, session: Session = Depends(get_session)):
    site.id = None
    session.add(site)
    session.commit()
    session.refresh(site)
    return site

@app.put("/api/v1/sites/{site_id}", response_model=MiningSite)
def update_site(site_id: int, updated_site: MiningSite, session: Session = Depends(get_session)):
    db_site = session.get(MiningSite, site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="الموقع غير موجود")
    db_site.name = updated_site.name
    db_site.state = updated_site.state
    db_site.coordinates = updated_site.coordinates
    db_site.is_active = updated_site.is_active
    session.add(db_site)
    session.commit()
    session.refresh(db_site)
    return db_site

@app.delete("/api/v1/sites/{site_id}")
def delete_site(site_id: int, session: Session = Depends(get_session)):
    db_site = session.get(MiningSite, site_id)
    if not db_site:
        raise HTTPException(status_code=404, detail="الموقع غير موجود")
    session.delete(db_site)
    session.commit()
    return {"message": "تم حذف الموقع بنجاح"}

# --- [2] عمليات المعدات والآليات (Equipment CRUD) ---
@app.get("/api/v1/equipment", response_model=List[Equipment])
def read_equipment(session: Session = Depends(get_session)):
    return session.exec(select(Equipment)).all()

@app.post("/api/v1/equipment", response_model=Equipment, status_code=201)
def create_equipment(item: Equipment, session: Session = Depends(get_session)):
    item.id = None
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.put("/api/v1/equipment/{eq_id}", response_model=Equipment)
def update_equipment(eq_id: int, updated_eq: Equipment, session: Session = Depends(get_session)):
    db_eq = session.get(Equipment, eq_id)
    if not db_eq:
        raise HTTPException(status_code=404, detail="المعدة غير موجودة")
    db_eq.name = updated_eq.name
    db_eq.owner = updated_eq.owner
    db_eq.status = updated_eq.status
    db_eq.last_maintenance = updated_eq.last_maintenance
    session.add(db_eq)
    session.commit()
    session.refresh(db_eq)
    return db_eq

# --- [3] مسارات الإنتاج وبث البيانات (Production) ---
@app.get("/api/v1/production", response_model=List[Production])
def read_production(session: Session = Depends(get_session)):
    return session.exec(select(Production)).all()

@app.post("/api/v1/production", response_model=Production, status_code=201)
def create_production(prod: Production, session: Session = Depends(get_session)):
    prod.id = None
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod

# --- [4] مسارات أسعار الذهب (Gold Prices) ---
@app.get("/api/v1/prices", response_model=List[GoldPrice])
def read_prices(session: Session = Depends(get_session)):
    return session.exec(select(GoldPrice)).all()

@app.post("/api/v1/prices", response_model=GoldPrice, status_code=201)
def update_gold_price(price: GoldPrice, session: Session = Depends(get_session)):
    price.id = None
    session.add(price)
    session.commit()
    session.refresh(price)
    return price

# --- [5] مسارات البلاغات والطوارئ (Reports) ---
@app.get("/api/v1/reports", response_model=List[Report])
def read_reports(session: Session = Depends(get_session)):
    return session.exec(select(Report)).all()

@app.post("/api/v1/reports", response_model=Report, status_code=201)
def create_report(report: Report, session: Session = Depends(get_session)):
    report.id = None
    session.add(report)
    session.commit()
    session.refresh(report)
    return report


# =======================================================
# التحديث الجديد: مسارات نظام طلبات وعروض المعدات (المخزن الافتراضي)
# =======================================================

# أ) مسارات طلبات المشترين (Equipment Orders)
@app.get("/api/v1/orders", response_model=List[EquipmentOrder])
def read_orders(session: Session = Depends(get_session)):
    return session.exec(select(EquipmentOrder)).all()

@app.post("/api/v1/orders", response_model=EquipmentOrder, status_code=201)
def create_order(order: EquipmentOrder, session: Session = Depends(get_session)):
    order.id = None
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

@app.put("/api/v1/orders/{order_id}/status", response_model=EquipmentOrder)
def update_order_status(order_id: int, status: str, session: Session = Depends(get_session)):
    order = session.get(EquipmentOrder, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="الطلب غير موجود")
    order.status = status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

# ب) مسارات عروض الأسعار السرية من التجار (Merchant Bids)
@app.get("/api/v1/bids/order/{order_id}", response_model=List[MerchantBid])
def read_bids_by_order(order_id: int, session: Session = Depends(get_session)):
    return session.exec(select(MerchantBid).where(MerchantBid.order_id == order_id)).all()

@app.post("/api/v1/bids", response_model=MerchantBid, status_code=201)
def create_bid(bid: MerchantBid, session: Session = Depends(get_session)):
    bid.id = None
    session.add(bid)
    session.commit()
    session.refresh(bid)
    return bid

@app.put("/api/v1/bids/{bid_id}/commission", response_model=MerchantBid)
def update_bid_commission_status(bid_id: int, status: str, session: Session = Depends(get_session)):
    bid = session.get(MerchantBid, bid_id)
    if not bid:
        raise HTTPException(status_code=404, detail="العرض غير موجود")
    bid.commission_status = status
    session.add(bid)
    session.commit()
    session.refresh(bid)
    return bid
