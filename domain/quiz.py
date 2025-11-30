from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config.db import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)

    questions = relationship("QuizQuestion", back_populates="quiz")
