from sqlalchemy import Column, Integer, String
from config.db import Base

class World(Base):
    __tablename__ = "worlds"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(2000), nullable=False)
