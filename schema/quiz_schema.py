from pydantic import BaseModel
from typing import List

class QuizAnswerResponse(BaseModel):
    id: int
    text: str

    class Config:
        from_attributes = True

class QuizQuestionResponse(BaseModel):
    id: int
    text: str
    max_choices: int
    answers: List[QuizAnswerResponse]

    class Config:
        from_attributes = True

class QuizResponse(BaseModel):
    id: int
    title: str
    questions: List[QuizQuestionResponse]

    class Config:
        from_attributes = True


class UserAnswerRequest(BaseModel):
    question_id: int
    answers: List[int]
