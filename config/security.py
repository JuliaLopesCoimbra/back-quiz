from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from domain.user import User

SECRET_KEY = "super_secret_key_change_later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30  # 30 dias

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload["sub"])
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "Usuário não encontrado")

    return user