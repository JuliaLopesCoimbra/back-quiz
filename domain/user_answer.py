from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    answer_id = Column(Integer, ForeignKey("quiz_answers.id"), nullable=False)
