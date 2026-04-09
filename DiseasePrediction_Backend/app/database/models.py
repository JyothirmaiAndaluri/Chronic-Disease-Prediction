from sqlalchemy import Column, Integer, String
from app.database.db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    phone = Column(String(15))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
class LoginLog(Base):
    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    login_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DiseaseLog(Base):
    __tablename__ = "disease_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    disease = Column(String(50))
    visit_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))