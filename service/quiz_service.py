from sqlalchemy.orm import Session
from repository.quiz_repository import QuizRepository
from fastapi import HTTPException, status

from service.quiz_rules import WORLD_ORDER, ANSWER_TO_WORLD


class QuizService:

    @staticmethod
    def get_quiz(db: Session, quiz_id: int):
        quiz = QuizRepository.get_quiz_with_questions(db, quiz_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz não encontrado")
        return quiz

    @staticmethod
    def save_user_answers(db: Session, user_id: int, question_id: int, answers: list):
        # salva cada resposta selecionada
        for ans in answers:
            QuizRepository.save_user_answer(
                db=db,
                user_id=user_id,
                question_id=question_id,
                answer_id=ans
            )
        return {"message": "Respostas salvas"}

    @staticmethod
    def finish_quiz(db: Session, user_id: int, quiz_id: int):

        quiz = QuizRepository.get_quiz_with_questions(db, quiz_id)
        if not quiz:
            raise HTTPException(404, "Quiz não encontrado")

        user_answers = QuizRepository.get_user_answers(db, user_id, quiz_id)

        if not user_answers:
            raise HTTPException(400, "Nenhuma resposta encontrada")

        # CONTADORES DOS MUNDOS
        world_points = {w: 0 for w in WORLD_ORDER}

        # Para cada resposta marcada pelo usuário
        for ans in user_answers:
            answer_text = ans.answer.text

            if answer_text not in ANSWER_TO_WORLD:
                continue  # segurança

            world = ANSWER_TO_WORLD[answer_text]
            world_points[world] += 1

        # ENCONTRAR O GANHADOR:
        # maior pontuação
        max_points = max(world_points.values())

        # filtrar os mundos que têm essa pontuação
        empatados = [w for w, pts in world_points.items() if pts == max_points]

        # REGRA OFICIAL: pega o primeiro mundo na ordem fixa
        winner = next(w for w in WORLD_ORDER if w in empatados)

        # salvar resultado
        QuizRepository.save_quiz_result(db, user_id, quiz_id, winner)

        return {"result": winner}