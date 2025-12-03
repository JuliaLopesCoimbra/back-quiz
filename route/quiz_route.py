from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from config.db import get_db
from controller.quiz_controller import QuizController
from schema.quiz_schema import QuizAnswerBatchRequest
from config.security import get_current_user

router = APIRouter(prefix="/quiz", tags=["Quiz"])


# -----------------------------------------------------
#  GET QUIZ (carrega perguntas e respostas)
# -----------------------------------------------------
@router.get("/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return QuizController.get_quiz(quiz_id, db)


# -----------------------------------------------------
#  START ATTEMPT — cria uma tentativa
# -----------------------------------------------------
@router.post("/{quiz_id}/start")
def start_attempt(
    quiz_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    return QuizController.start_attempt(quiz_id, user.id, db)


# -----------------------------------------------------
#  SAVE ANSWERS (BATCH) — salva todas as respostas de uma vez
# -----------------------------------------------------
@router.post("/{quiz_id}/{attempt_id}/answers")
def send_answers_batch(
    quiz_id: int,
    attempt_id: int,
    body: QuizAnswerBatchRequest,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    return QuizController.save_answers_batch(
        quiz_id=quiz_id,
        attempt_id=attempt_id,
        user_id=user.id,
        body=body,
        db=db
    )


# -----------------------------------------------------
#  FINISH ATTEMPT — finaliza a rodada do usuário
# -----------------------------------------------------
@router.post("/{quiz_id}/{attempt_id}/finish")
def finish_attempt(
    quiz_id: int,
    attempt_id: int,
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token, db)

    return QuizController.finish_attempt(
        quiz_id=quiz_id,
        attempt_id=attempt_id,
        user_id=user.id,
        db=db
    )
