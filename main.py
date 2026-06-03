from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

# إجبار قاعدة البيانات على مسح الجداول القديمة وبنائها من جديد بنظام الأعمدة الجديد
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sudan Mining Platform API",
    description="المنصة السودانية للتعدين - لوحة التحكم الخلفية",
    version="1.0.0"
)

# إعدادات الـ CORS لتسمح للواجهات بالاتصال بالسيرفر دون قيود
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to Sudan Mining Platform API"}

# نافذة تسجيل الحساب الجديد باللغة العربية المتوافقة مع الموديل الجديد
@app.post("/api/v1/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # التحقق من عدم تكرار البريد الإلكتروني
    db_user_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user_email:
        raise HTTPException(
            status_code=400,
            detail="البريد الإلكتروني مسجل بالفعل بالنظام"
        )
    
    # التحقق من عدم تكرار اسم المستخدم
    db_user_username = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user_username:
        raise HTTPException(
            status_code=400,
            detail="اسم المستخدم مأخوذ بالفعل، اختر اسماً آخر"
        )
    
    # إنشاء الحساب الجديد وحفظه
    new_user = models.User(
        username=user.username,
        email=user.email,
        password=user.password  # سيتم ربط التشفير لاحقاً عند استقرار الاتصال
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
