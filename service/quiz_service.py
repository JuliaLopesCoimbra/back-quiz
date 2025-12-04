from sqlalchemy.orm import Session
from repository.quiz_repository import QuizRepository
from fastapi import HTTPException
from service.quiz_rules import ANSWER_TO_WORLD, WORLD_TO_ID


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
            worlds = ANSWER_TO_WORLD.get(answer_text, [])

            # soma 1 ponto para cada mundo possível
            for w in worlds:
                world_points[w] = world_points.get(w, 0) + 1

        # Encontrar a maior pontuação
        max_points = max(world_points.values())
        empatados = [w for w, p in world_points.items() if p == max_points]

        # Desempate pela ORDEM REAL das respostas do usuário
        winner = None

        for ans in user_answers:
            answer_text = ans.answer.text
            worlds = ANSWER_TO_WORLD.get(answer_text, [])

            for w in worlds:
                if w in empatados:
                    winner = w
                    break

            if winner:
                break

        # Salvar resultado final
        QuizRepository.save_quiz_result(db, user_id, quiz_id, winner)

        world_id = WORLD_TO_ID.get(winner)
        image_url = f"https://fotoai-picbrand.s3.sa-east-1.amazonaws.com/quiz/{world_id}.png"

        return {
            "result": winner,
            "image_url": image_url
        }

    # ------------------------------- BATCH MODE -------------------------------

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

    # ------------------------------- START ATTEMPT -------------------------------

    def start_attempt(db, user_id, quiz_id):
        return QuizRepository.create_attempt(db, user_id, quiz_id)

    # ------------------------------- FINISH ATTEMPT -------------------------------

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

        # Soma de pontos considerando múltiplos mundos
        for ans in answers:
            answer_text = ans.answer.text
            worlds = ANSWER_TO_WORLD.get(answer_text, [])

            for w in worlds:
                world_points[w] = world_points.get(w, 0) + 1

        # Verificar maior pontuação
        max_points = max(world_points.values())
        empatados = [w for w, p in world_points.items() if p == max_points]

        # Desempate pela ordem REAL
        winner = None

        for ans in answers:
            answer_text = ans.answer.text
            worlds = ANSWER_TO_WORLD.get(answer_text, [])

            for w in worlds:
                if w in empatados:
                    winner = w
                    break

            if winner:
                break

        print("DEBUG -----------------------------------")
        for ans in answers:
            print(
                "ID:", ans.answer.id,
                " | TEXTO:", ans.answer.text,
                " | MUNDOS:", ANSWER_TO_WORLD.get(ans.answer.text)
            )
        print("DEBUG -----------------------------------")

        # Finaliza tentativa
        QuizRepository.finish_attempt(db, attempt_id)

        # Salva resultado final
        QuizRepository.save_quiz_result(
            db=db,
            user_id=user_id,
            quiz_id=attempt.quiz_id,
            result=winner
        )

        world_id = WORLD_TO_ID.get(winner)
        image_url = f"https://fotoai-picbrand.s3.sa-east-1.amazonaws.com/quiz/{world_id}.png"

        return {
            "result": winner,
            "image_url": image_url
        }
