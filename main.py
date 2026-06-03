from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import models, database
from database import engine, get_db

# إنشاء الجداول في قاعدة البيانات تلقائياً عند الإقلاع
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.get("/")
def read_root():
    return {"status": "running", "database": "connected"}

@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # التحقق من عدم تكرار البريد الإلكتروني
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # تشفير كلمة المرور وحفظ المستخدم
    hashed_pwd = pwd_context.hash(password)
    new_user = models.User(username=username, email=email, hashed_password=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}
