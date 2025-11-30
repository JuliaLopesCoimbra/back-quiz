from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.db import get_db
from controller.user_controller import register_user_controller
from schema.user_schema import UserCreate, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=TokenResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return register_user_controller(user, db)
