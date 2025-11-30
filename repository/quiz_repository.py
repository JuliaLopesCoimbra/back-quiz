from sqlalchemy.orm import Session
from domain.quiz import Quiz
from domain.user_answer import UserAnswer

class QuizRepository:

    @staticmethod
    def get_quiz_with_questions(db: Session, quiz_id: int):
        return db.query(Quiz).filter(Quiz.id == quiz_id).first()

    @staticmethod
    def save_user_answer(db: Session, user_id: int, question_id: int, answer_id: int):
        user_answer = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            answer_id=answer_id
        )
        db.add(user_answer)
        db.commit()
        db.refresh(user_answer)
        return user_answer
