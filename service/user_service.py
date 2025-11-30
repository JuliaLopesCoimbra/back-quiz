from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from config.security import create_access_token
from fastapi import HTTPException, status

class UserService:

    @staticmethod
    def create_user(db: Session, name: str, email: str):
        existing = UserRepository.get_by_email(db, email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado."
            )

        user = UserRepository.create(db, name, email)

        token = create_access_token({"sub": str(user.id)})

        return user, token
