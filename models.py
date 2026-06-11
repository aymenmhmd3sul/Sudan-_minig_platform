from sqlalchemy import Column, Integer, String, Float, Boolean, Text, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class BuyerRequest(Base):
    __tablename__ = 'buyer_requests'

    id = Column(Integer, primary_key=True)
    buyer_name = Column(String)
    whatsapp = Column(String)
    category = Column(String)
    specs = Column(Text)
    status = Column(String, default='new')
    created_at = Column(String, default=str(datetime.utcnow()))
