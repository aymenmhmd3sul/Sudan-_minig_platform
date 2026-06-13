from fastapi import FastAPI

app = FastAPI(title="Sudan Mining Hub API")

@app.get("/")
def root():
    return {"status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}
