from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import models
from database import engine, get_db

# إعدادات التشفير ومفاتيح الأمان
SECRET_KEY = "SUDAN_MINING_SUPER_SECRET_KEY_2026" # مفتاح لتوقيع الـ Tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# إنشاء الجداول تلقائياً
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sudan Mining Hub API")

# الدالة المساعدة لإنشاء توكن الأمان (JWT)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# الدالة المساعدة للتحقق من هوية المستخدم الحالي عبر التوكن
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def read_root():
    return {"status": "running", "database": "connected"}


# --- النافذة 1: تسجيل حساب جديد ---
@app.post("/api/v1/register", status_code=status.HTTP_201_CREATED)
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_pwd = pwd_context.hash(password)
    new_user = models.User(username=username, email=email, hashed_password=hashed_pwd, role="viewer")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}


# --- النافذة 2: تسجيل الدخول والحصول على التوكن (Login) ---
@app.post("/api/v1/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- 3 النافذة : استعراض الملف الشخصي (Profile) ---
@app.get("/api/v1/profile")
def get_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "created_at": current_user.created_at
    }


# --- النافذة 4: تحديث الصلاحيات والأدوار (Update Role) ---
@app.put("/api/v1/update-role")
def update_user_role(target_username: str, new_role: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # حماية المسار: لا يسمح بتغيير الأدوار إلا لمن رتبته admin
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to change roles")
    
    user_to_update = db.query(models.User).filter(models.User.username == target_username).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="User not found")
    
    if new_role not in ["admin", "supervisor", "agent", "viewer"]:
        raise HTTPException(status_code=400, detail="Invalid role specified")
        
    user_to_update.role = new_role
    db.commit()
    return {"message": f"Role updated successfully for {target_username} to {new_role}"}
