from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base
from sqlalchemy.orm import relationship

class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    answer_id = Column(Integer, ForeignKey("quiz_answers.id"))

    attempt = relationship("QuizAttempt", back_populates="answers")
    answer = relationship("QuizAnswer")
