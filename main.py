from fastapi import FastAPI
from sqlalchemy.orm import Session
import database
import models

app = FastAPI()

@app.get("/api/v1/market/items")
def get_items():
    try:
        with Session(database.engine) as session:
            items = session.query(models.MarketItem).all()

            return {
                "count": len(items),
                "data": [
                    {
                        "id": i.id,
                        "price": getattr(i, "price", None),
                        "status": getattr(i, "status", None)
                    }
                    for i in items
                ]
            }

    except Exception as e:
        return {"error": str(e)}
