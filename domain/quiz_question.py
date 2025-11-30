from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    text = Column(String(500), nullable=False)
    max_choices = Column(Integer, default=1)  # 1 = normal, 2 = multipla

    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question")
