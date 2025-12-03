from sqlalchemy.orm import Session
from repository.quiz_repository import QuizRepository
from fastapi import HTTPException, status
from service.quiz_rules import WORLD_ORDER, ANSWER_TO_WORLD, WORLD_TO_ID


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
        existing_result = QuizRepository.get_user_quiz_result(db, user_id, quiz_id)
        if existing_result:
            raise HTTPException(
                status_code=400,
                detail="Você já finalizou este quiz"
            )

        quiz = QuizRepository.get_quiz_with_questions(db, quiz_id)
        if not quiz:
            raise HTTPException(404, "Quiz não encontrado")

        user_answers = QuizRepository.get_user_answers(db, user_id, quiz_id)

        if not user_answers:
            raise HTTPException(400, "Nenhuma resposta encontrada")

        # soma de pontos por mundo
        world_points = {}

        for ans in user_answers:
            answer_text = ans.answer.text
            world = ANSWER_TO_WORLD.get(answer_text)
            if world:
                world_points[world] = world_points.get(world, 0) + 1

        # Encontrar a maior pontuação
        max_points = max(world_points.values())
        empatados = [w for w, p in world_points.items() if p == max_points]

        # Desempate pela ordem REAL das respostas do usuário
        #
        # A ordem está natural na tabela user_answers
        # pois cada insert foi feito na ordem em que ele respondeu.
        #
        for ans in user_answers:
            answer_text = ans.answer.text
            mundo = ANSWER_TO_WORLD.get(answer_text)
            if mundo in empatados:
                winner = mundo
                break

        # Salvar resultado
        QuizRepository.save_quiz_result(db, user_id, quiz_id, winner)

        # Depois de calcular 'winner' e salvar no banco
        world_id = WORLD_TO_ID.get(winner)

        image_url = f"https://fotoai-picbrand.s3.sa-east-1.amazonaws.com/quiz/{world_id}.png"

        return {
            "result": winner,
            "image_url": image_url
        }

    def save_answers_batch(db, attempt_id, user_id, data):
        attempt = QuizRepository.get_attempt(db, attempt_id, user_id)
        if not attempt:
            raise HTTPException(404, "Tentativa não encontrada")

        if attempt.finished:
            raise HTTPException(400, "Esta tentativa já foi finalizada")

        # apagar respostas antigas da attempt
        QuizRepository.delete_attempt_answers(db, attempt_id)

        for item in data:
            for ans in item.answers:
                QuizRepository.save_user_answer(
                    db=db,
                    attempt_id=attempt_id,
                    user_id=user_id,
                    question_id=item.question_id,
                    answer_id=ans
                )

        return {"message": "Respostas salvas com sucesso"}

    def start_attempt(db, user_id, quiz_id):
        return QuizRepository.create_attempt(db, user_id, quiz_id)

    def finish_attempt(db, attempt_id, user_id):

        attempt = QuizRepository.get_attempt(db, attempt_id, user_id)
        if not attempt:
            raise HTTPException(404, "Tentativa não encontrada")

        if attempt.finished:
            raise HTTPException(400, "Esta tentativa já foi finalizada")

        answers = QuizRepository.get_attempt_answers(db, attempt_id)
        if not answers:
            raise HTTPException(400, "Nenhuma resposta enviada")

        world_points = {}

        for ans in answers:
            world = ANSWER_TO_WORLD.get(ans.answer.text)
            if world:
                world_points[world] = world_points.get(world, 0) + 1

        max_points = max(world_points.values())
        tied = [w for w, p in world_points.items() if p == max_points]

        # desempate: primeira resposta da attempt
        for ans in answers:
            world = ANSWER_TO_WORLD.get(ans.answer.text)
            if world in tied:
                winner = world
                break

        # MARCA attempt como finalizada
        QuizRepository.finish_attempt(db, attempt_id)

        # SALVA O RESULTADO NA user_quiz_results
        QuizRepository.save_quiz_result(
            db=db,
            user_id=user_id,
            quiz_id=attempt.quiz_id,
            result=winner
        )

        # Depois de calcular 'winner' e salvar no banco
        world_id = WORLD_TO_ID.get(winner)

        image_url = f"https://fotoai-picbrand.s3.sa-east-1.amazonaws.com/quiz/{world_id}.png"

        return {
            "result": winner,
            "image_url": image_url
        }



