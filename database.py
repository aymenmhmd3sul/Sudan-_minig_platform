import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    DATABASE_URL = 'sqlite:///local.db'

if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

connect_args = {}
if 'postgresql' in DATABASE_URL:
    connect_args = {'sslmode': 'require'}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    Base.metadata.create_all(engine)
