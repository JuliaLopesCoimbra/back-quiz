from sqlalchemy.orm import Session
from schema.quiz_schema import UserAnswerRequest, QuizResponse
from service.quiz_service import QuizService

class QuizController:

    @staticmethod
    def get_quiz(quiz_id: int, db: Session) -> QuizResponse:
        quiz = QuizService.get_quiz(db, quiz_id)
        return quiz  # Pydantic converte automático pelo from_attributes

    @staticmethod
    def save_answers(quiz_id: int, user_id: int, body: UserAnswerRequest, db: Session):
        return QuizService.save_user_answers(
            db=db,
            user_id=user_id,
            question_id=body.question_id,
            answers=body.answers
        )

    @staticmethod
    def finish_quiz(quiz_id: int, user_id: int, db: Session):
        return QuizService.finish_quiz(db, user_id, quiz_id)

    @staticmethod
    def save_answers_batch(quiz_id, attempt_id, user_id, body, db):
        return QuizService.save_answers_batch(
            db=db,
            attempt_id=attempt_id,
            user_id=user_id,
            data=body.answers
        )

    def start_attempt(quiz_id, user_id, db):
        attempt = QuizService.start_attempt(db, user_id, quiz_id)
        return {"attempt_id": attempt.id}

    def finish_attempt(quiz_id, attempt_id, user_id, db):
        return QuizService.finish_attempt(db, attempt_id, user_id)

