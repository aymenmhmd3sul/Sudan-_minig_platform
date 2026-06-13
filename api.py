from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "SERVER IS ALIVE"}

@app.get("/api/v1/market/items")
def items():
    return {"status": "OK - CLEAN START"}
