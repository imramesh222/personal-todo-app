from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.repo.datasource import Base

class UserRecord(Base):
    __tablename__ = "users"
    id = Column(String(255), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
