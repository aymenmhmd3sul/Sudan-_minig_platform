import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    with engine.connect() as conn:
        print("==========================================")
        print("🚀 DATABASE CONNECTED SUCCESSFULLY IN RENDER!")
        print("==========================================")
except Exception as e:
    print("==========================================")
    print(f"❌ DATABASE CONNECTION FAILED: {e}")
    print("==========================================")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
