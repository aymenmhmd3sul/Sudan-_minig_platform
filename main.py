from fastapi import FastAPI
import sqlite3

app = FastAPI()

@app.get("/api/v1/market/items")
def get_items():
    try:
        conn = sqlite3.connect("local.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM market_items")
        rows = cursor.fetchall()

        return {
            "count": len(rows),
            "data": rows
        }

    except Exception as e:
        return {"error": str(e)}
