from sqlalchemy.orm import Session
from repository.user_repository import UserRepository, UserEntranceRepository
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

    @staticmethod
    def create_or_enter_user(db: Session, name: str, email: str):
        # Se já existe, não barrar
        user = UserRepository.get_by_email(db, email)

        if not user:
            # Criar novo usuário
            user = UserRepository.create(db, name, email)

        # Registrar entrada
        UserEntranceRepository.create_entrance(db, user.id)

        # Gerar token
        token = create_access_token({"sub": str(user.id)})

        return user, token
