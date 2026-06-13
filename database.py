import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set in environment variables")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    Base.metadata.create_all(engine)
