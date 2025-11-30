from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from config.db import get_db
from controller.quiz_controller import QuizController
from schema.quiz_schema import UserAnswerRequest
from config.security import get_current_user
from schema.user_schema import UserResponse

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.get("/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return QuizController.get_quiz(quiz_id, db)


@router.post("/{quiz_id}/answer")
def send_answer(
        quiz_id: int,
        body: UserAnswerRequest,
        authorization: str = Header(...),
        db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    return QuizController.save_answers(quiz_id, user.id, body, db)
