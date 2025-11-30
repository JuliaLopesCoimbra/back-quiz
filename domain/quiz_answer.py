from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    text = Column(String(200), nullable=False)

    question = relationship("QuizQuestion", back_populates="answers")
