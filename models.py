from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

# 1. جدول مواقع التعدين (توسيع الحقول حسب مقترحك)
class MiningSite(SQLModel, table=True):
    __tablename__ = "mining_sites"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    state: str # الولاية
    coordinates: Optional[str] = None # الإحداثيات (GPS)
    is_active: bool = Field(default=True)

# 2. جدول المعدات والآليات
class Equipment(SQLModel, table=True):
    __tablename__ = "equipment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str # اسم المعدة
    owner: str # المالك
    status: str = Field(default="active") # الحالة التشغيلية
    last_maintenance: Optional[str] = None # تاريخ الصيانة

# 3. جدول الإنتاجية اليومية
class Production(SQLModel, table=True):
    __tablename__ = "production"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    site_id: int # ربط بالموقع
    ore_weight: float # كمية الخام (بالطن مثلاً)
    gold_weight: float # كمية الذهب المستخلص (بالجرام)
    date: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))

# 4. جدول أسعار الذهب والعملات
class GoldPrice(SQLModel, table=True):
    __tablename__ = "gold_prices"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    local_price: float # السعر المحلي للجرام
    global_ounce: float # سعر الأونصة العالمي
    usd_rate: float # سعر الدولار مقابل الجنيه
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

# 5. جدول البلاغات والطوارئ للميدان
class Report(SQLModel, table=True):
    __tablename__ = "reports"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    site_id: int
    report_type: str # (أعطال، سرقات، مخالفات، طلب صيانة)
    details: str # تفاصيل البلاغ
    status: str = Field(default="pending") # (قيد المراجعة، تم الحل)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d %H:%M"))
