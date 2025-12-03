from sqlalchemy.orm import Session
from domain.entrance import UserEntrance
from domain.user import User

class UserRepository:
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, name: str, email: str):
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

class UserEntranceRepository:
    @staticmethod
    def create_entrance(db: Session, user_id: int):
        item = UserEntrance(user_id=user_id)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item