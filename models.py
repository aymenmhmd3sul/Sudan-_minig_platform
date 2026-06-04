from typing import Optional
from sqlmodel import SQLModel, Field

# 1. جدول مواقع التعدين (Mining Sites)
class MiningSite(SQLModel, table=True):
    __tablename__ = "mining_sites"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: str
    is_active: bool = Field(default=True)

# 2. جدول المعدات والآليات (Equipment)
class Equipment(SQLModel, table=True):
    __tablename__ = "equipment"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    status: str = Field(default="active")
