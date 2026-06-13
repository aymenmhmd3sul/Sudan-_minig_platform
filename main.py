from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select
import database
import models

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(database.engine)

@app.get("/api/v1/market/items")
def get_items():
    try:
        with Session(database.engine) as session:
            items = session.exec(select(models.MarketItem)).all()
            return {
                "count": len(items),
                "data": items
            }
    except Exception as e:
        return {"error": str(e)}
