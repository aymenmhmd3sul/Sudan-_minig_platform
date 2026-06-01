from fastapi import FastAPI

app = FastAPI(
    docs_url="/docs",
    redoc_url=None
)

@app.get("/")
def root():
    return {"message": "Sudan Mining Hub is running"}
