from fastapi import FastAPI
import database
import models

app = FastAPI()

@app.get("/api/v1/market/items")
def get_items():
    try:
        with database.SessionLocal() as session:
            items = session.exec(models.MarketItem.__table__.select()).fetchall()

            return {
                "count": len(items),
                "data": [dict(i._mapping) for i in items]
            }

    except Exception as e:
        return {"error": str(e)}
