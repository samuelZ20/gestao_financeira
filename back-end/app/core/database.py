import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()  # lê o arquivo .env

#conexao com o postgress
engine = create_engine(os.getenv("DATABASE_URL"))
#conversa com o banco
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass