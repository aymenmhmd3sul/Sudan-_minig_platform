import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

# استيراد المكونات المباشرة من ملفاتك المحلية في الجذر
import models
from database import engine, Base, get_db

# إنشاء الجداول عند الإقلاع بناءً على الاستيراد النظيف
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sudan Mining Hub")

# الـ Schema المطلوبة للتسجيل تم صياغتها بـ str عادي لتفادي كسر الإقلاع بسبب email-validator
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- بداية الكود الخاص بك بعد ضبط الاستيرادات والوسائط ---

@app.post("/api/v1/register", response_model=UserResponse)
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # 1. التحقق من عدم تكرار البريد الإلكتروني
    db_user_email = db.query(models.User).filter(models.User.email == email).first()
    if db_user_email:
        raise HTTPException(
            status_code=400,
            detail="البريد الإلكتروني مسجل بالفعل بالنظام"
        )
        
    # 2. التحقق من عدم تكرار اسم المستخدم
    db_user_username = db.query(models.User).filter(models.User.username == username).first()
    if db_user_username:
        raise HTTPException(
            status_code=400,
            detail="اسم المستخدم مأخوذ بالفعل، اختر اسماً آخر"
        )
        
    # 3. إنشاء الحساب وحفظه في الحقل المسمى hashed_password داخل models.py
    # (ملاحظة هندسية: سيتم إضافة التشفير لاحقاً عبر passlib بمجرد استقرار الإقلاع)
    new_user = models.User(
        username=username,
        email=email,
        hashed_password=password  
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"حدث خطأ داخلي أثناء حفظ البيانات: {str(e)}"
        )
