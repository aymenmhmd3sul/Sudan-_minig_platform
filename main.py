from fastapi import FastAPI
from sqlalchemy.orm import Session
import models
import database

app = FastAPI()

@app.get("/api/v1/market/items")
def get_items():
    try:
        with Session(database.engine) as session:
            items = session.query(models.MarketItem).all()
            return [
                {
                    "id": x.id,
                    "price": getattr(x, "price", None),
                    "status": getattr(x, "status", None)
                }
                for x in items
            ]
    except Exception as e:
        return {"error": str(e)}
