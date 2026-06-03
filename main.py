# نافذة تسجيل الحساب المتوافقة مع إرسال البيانات عبر الرابط (Query Parameters)
@app.post("/api/v1/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    # التحقق من عدم تكرار البريد الإلكتروني
    db_user_email = db.query(models.User).filter(models.User.email == email).first()
    if db_user_email:
        raise HTTPException(
            status_code=400,
            detail="البريد الإلكتروني مسجل بالفعل بالنظام"
        )
    
    # التحقق من عدم تكرار اسم المستخدم
    db_user_username = db.query(models.User).filter(models.User.username == username).first()
    if db_user_username:
        raise HTTPException(
            status_code=400,
            detail="اسم المستخدم مأخوذ بالفعل، اختر اسماً آخر"
        )
    
    # إنشاء الحساب الجديد وحفظه
    new_user = models.User(
        username=username,
        email=email,
        password=password
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
