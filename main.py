from fastapi import FastAPi, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlachemy.orm import Session
import models, database

app = FastAPY(title="Sudan Mining Hub API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.SQLModel.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/api/v1/market/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(models.MarketItem).all()

@app.get("/api/v1/prices")
def get_prices():
    return {
        "local_price": 114842,
        "global_price": 75.56,
        "direction": "مצ��رк",
        "change": 0,
        "history": [114700, 114750, 114800, 114850]
    }
