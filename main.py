from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI(title="Sudan Mining Hub API")

# مؤقتًا (سنربطه بDB لاحقًا)
engine = create_engine("sqlite:///./local.db")

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/market/items")
def get_items():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as id, 'gold' as name"))
            rows = result.fetchall()

        return {
            "count": len(rows),
            "data": [dict(r._mapping) for r in rows]
        }

    except Exception as e:
        return {"error": str(e)}
