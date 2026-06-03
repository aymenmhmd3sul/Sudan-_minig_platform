import os
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

# استيراد المكونات المحلية المستقرة من مشروعك
import models
from database import engine, Base, get_db

# إنشاء الجداول تلقائياً عند الإقلاع
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sudan Mining Hub")

# صياغة نموذج الاستجابة داخلياً لقطع الشك باليقين وتجنب غياب schemas.py
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# نافذة تسجيل الحساب المتوافقة تماماً مع تعديلاتك الأخيرة (Query Parameters)
@app.post("/api/v1/register", response_model=UserResponse, status_code=201)
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    
    # 1. التحقق من عدم تكرار البريد الإلكتروني (تم الإصلاح بناءً على صورتك المحدثة)
    db_user_email = db.query(models.User).filter(models.User.email == email).first()
    if db_user_email:
        raise HTTPException(
            status_code=400,
            detail="البريد الإلكتروني مسجل بالفعل بالنظام"
        )
        
    # 2. التحقق من عدم تكرار اسم المستخدم (تم الإصلاح بناءً على صورتك المحدثة)
    db_user_username = db.query(models.User).filter(models.User.username == username).first()
    if db_user_username:
        raise HTTPException(
            status_code=400,
            detail="اسم المستخدم مأخوذ بالفعل، اختر اسماً آخر"
        )
        
    # 3. إنشاء الحساب وحفظه في الحقل المسمى hashed_password داخل models.py الخاص بك
    new_user = models.User(
        username=username,
        # تم تصحيح أسماء المتغيرات هنا لتطابق المدخلات المباشرة للدالة
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
