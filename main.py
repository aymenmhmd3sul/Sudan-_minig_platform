from fastapi import FastAPI
import database
import models

app = FastAPI()

@app.get("/api/v1/market/items")
def get_items():
    try:
        return {
            "models_loaded": str(models.MarketItem),
            "table": str(models.MarketItem.__table__)
        }
    except Exception as e:
        return {"startup_error": str(e)}
