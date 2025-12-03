from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Exemplo de URL do MySQL (troque pelos seus dados)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:10203011Julia@localhost:3306/quizdb"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=280
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency global para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
