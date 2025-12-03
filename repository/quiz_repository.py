from sqlalchemy.orm import Session, joinedload
from domain.quiz import Quiz
from domain.quiz_attempts import QuizAttempt
from domain.quiz_question import QuizQuestion
from domain.quiz_answer import QuizAnswer
from domain.user_answer import UserAnswer
from domain.user_quiz_result import UserQuizResult
from sqlalchemy import select, delete

class QuizRepository:

    @staticmethod
    def get_quiz_with_questions(db: Session, quiz_id: int):
        return (
            db.query(Quiz)
            .options(
                joinedload(Quiz.questions)
                .joinedload(QuizQuestion.answers)
            )
            .filter(Quiz.id == quiz_id)
            .first()
        )

    @staticmethod
    def save_user_answer(db, attempt_id, user_id, question_id, answer_id):
        item = UserAnswer(
            attempt_id=attempt_id,
            user_id=user_id,
            question_id=question_id,
            answer_id=answer_id
        )
        db.add(item)
        db.commit()

    @staticmethod
    def get_user_answers(db: Session, user_id: int, quiz_id: int):
        return (
            db.query(UserAnswer)
            .join(QuizQuestion)
            .filter(
                UserAnswer.user_id == user_id,
                QuizQuestion.quiz_id == quiz_id
            )
            .all()
        )

    @staticmethod
    def save_quiz_result(db: Session, user_id: int, quiz_id: int, result: str):
        item = UserQuizResult(
            user_id=user_id,
            quiz_id=quiz_id,
            result=result
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_user_quiz_result(db: Session, user_id: int, quiz_id: int):
        return (
            db.query(UserQuizResult)
            .filter(
                UserQuizResult.user_id == user_id,
                UserQuizResult.quiz_id == quiz_id
            )
            .first()
        )

    @staticmethod
    def delete_user_answers(db: Session, user_id: int, quiz_id: int):
        question_ids = (
            db.query(QuizQuestion.id)
            .filter(QuizQuestion.quiz_id == quiz_id)
            .all()
        )

        question_ids = [q[0] for q in question_ids]

        db.query(UserAnswer).filter(
            UserAnswer.user_id == user_id,
            UserAnswer.question_id.in_(question_ids)
        ).delete(synchronize_session=False)

        db.commit()

    @staticmethod
    def create_attempt(db: Session, user_id: int, quiz_id: int):
        attempt = QuizAttempt(user_id=user_id, quiz_id=quiz_id)
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt

    @staticmethod
    def get_attempt(db: Session, attempt_id: int, user_id: int):
        return db.query(QuizAttempt).filter(
            QuizAttempt.id == attempt_id,
            QuizAttempt.user_id == user_id
        ).first()

    @staticmethod
    def get_attempt_answers(db, attempt_id):
        return db.query(UserAnswer).filter(
            UserAnswer.attempt_id == attempt_id
        ).all()

    @staticmethod
    def finish_attempt(db, attempt_id):
        db.query(QuizAttempt).filter(
            QuizAttempt.id == attempt_id
        ).update({"finished": True})
        db.commit()

    @staticmethod
    def delete_attempt_answers(db: Session, attempt_id: int):
        db.query(UserAnswer).filter(
            UserAnswer.attempt_id == attempt_id
        ).delete(synchronize_session=False)

        db.commit()
