from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI(title="Sudan Mining Hub API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to Sudan Mining Hub API"}

@app.post("/api/v1/market/items", response_model=schemas.MarketItem)
def create_item(item: schemas.MarketItemCreate, db: Session = Depends(get_db)):
    db_item = models.MarketItem(
        title=item.title,
        category=item.category,
        price=item.price,
        specs=item.specs,
        whatsapp=item.whatsapp,
        owner_name=item.owner_name
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/api/v1/market/items", response_model=list[schemas.MarketItem])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.MarketItem).all()
    return items

@app.get("/api/v1/prices")
def get_prices():
    return {
        "local_price": 114842,
        "global_price": 75.56,
        "direction": "مستقر",
        "change": 0,
        "history": [
            114700, 114750, 114800, 114850, 114900, 114870, 114920, 114842
        ]
    }
