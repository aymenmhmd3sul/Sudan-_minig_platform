from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Session, select
from fastapi.middleware.cors import CORSMiddleware

# استيراد محرك الاتصال والجلسة من ملف الـ database
from database import engine, get_session
# استيراد الموديلات الهيكلية الفتحية من ملف الـ models
from models import MiningSite, Equipment

# إعداد التطبيق والواجهات الأساسية
app = FastAPI(
    title="Sudan Mining Hub - منصة تعدين السودان الرقمية",
    description="البنية الخلفية المستقرة والمربوطة بقاعدة البيانات السحابية لإدارة المواقع والآليات.",
    version="1.1.0"
)

# تفعيل الـ CORS لضمان إمكانية الاتصال من تطبيقات الويب والموبايل مستقبلاً
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# حدث بدء التشغيل: إنشاء الجداول تلقائياً وبث البيانات التجريبية الأساسية إن كانت قاعدة البيانات فارغة
@app.on_event("startup")
def on_startup():
    # هذا الأمر ينشئ جداول mining_sites و equipment في PostgreSQL فوراً إذا لم تكن موجودة
    SQLModel.metadata.create_all(engine)
    
    # بث بيانات أولية كـ Mock Data في الجداول الحقيقية عند أول تشغيل فقط
    with Session(engine) as session:
        if not session.exec(select(MiningSite)).first():
            site1 = MiningSite(name="موقع أبو حمد الرئيسي", location="ولاية نهر النيل")
            site2 = MiningSite(name="موقع وادي حلفا", location="الولاية الشمالية")
            session.add(site1)
            session.add(site2)
            session.commit()

# --- مسارات الـ API (Endpoints) المحدثة لتقرأ وتكتب من قاعدة البيانات ---

@app.get("/", tags=["الرئيسية"])
def read_root():
    return {"status": "online", "message": "Welcome to Sudan Mining Hub API Connected to PostgreSQL"}

# 1. جلب كل مواقع التعدين
@app.get("/api/v1/mining/sites", response_model=List[MiningSite], tags=["م مواقع التعدين"])
def get_mining_sites(session: Session = Depends(get_session)):
    sites = session.exec(select(MiningSite)).all()
    return sites

# 2. جلب موقع تعدين محدد عبر الـ ID
@app.get("/api/v1/mining/sites/{site_id}", response_model=MiningSite, tags=["مواقع التعدين"])
def get_mining_site_by_id(site_id: int, session: Session = Depends(get_session)):
    site = session.get(MiningSite, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Mining site not found")
    return site

# 3. جلب كل المعدات والآليات
@app.get("/api/v1/equipment", response_model=List[Equipment], tags=["المعدات والآليات"])
def get_all_equipment(session: Session = Depends(get_session)):
    equipments = session.exec(select(Equipment)).all()
    return equipments

# 4. إضافة معدة جديدة (وهنا سيتولى PostgreSQL توليد الـ ID تلقائياً واختفاء الـ null)
@app.post("/api/v1/equipment", response_model=Equipment, status_code=201, tags=["المعدات والآليات"])
def create_equipment(equipment_data: Equipment, session: Session = Depends(get_session)):
    # تصفير الـ id لضمان أن قاعدة البيانات هي من ستولد الرقم التسلسلي الفريد
    equipment_data.id = None
    session.add(equipment_data)
    session.commit()
    session.refresh(equipment_data) # جلب البيانات بعد حقن الـ ID الجديد من قاعدة البيانات
    return equipment_data
