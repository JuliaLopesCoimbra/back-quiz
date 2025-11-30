from fastapi import FastAPI
from config.db import Base, engine

# IMPORTAR MODELS ANTES DO create_all
from domain.user import User
from domain.quiz import Quiz
from domain.quiz_question import QuizQuestion
from domain.quiz_answer import QuizAnswer
from domain.user_answer import UserAnswer
from domain.world import World
Base.metadata.create_all(bind=engine)

# Rotas
from route.user_route import router as user_router

app = FastAPI()

app.include_router(user_router)
