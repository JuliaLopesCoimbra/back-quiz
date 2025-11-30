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
