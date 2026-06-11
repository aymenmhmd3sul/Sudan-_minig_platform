from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models, database

app = FastAPI(title="Mining API")

class RequestIn(BaseModel):
    buyer_name: str
    whatsapp: str
    category: str
    specs: str

@app.post('/request')
def create_request(data: RequestIn):
    with Session(database.engine) as session:
        req = models.BuyerRequest(
            buyer_name=data.buyer_name,
            whatsapp=data.whatsapp,
            category=data.category,
            specs=data.specs
        )
        session.add(req)
        session.commit()
        session.refresh(req)
        return {'status': 'created', 'id': req.id}

@app.get('/')
def root():
    return {'status': 'API running'}
