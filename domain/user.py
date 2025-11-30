from sqlalchemy import Column, Integer, String, DateTime, func
from config.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(200), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
