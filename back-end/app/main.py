from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, SessionLocal, engine
from app.models import Teste

Base.metadata.create_all(bind=engine)  # cria as tabelas que ainda não existem

app = FastAPI(title="Meu Bolso API")

# Deixa o front-end (porta 5173) chamar esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def hello():
    return {"mensagem": "Olá do Meu Bolso!"}


@app.post("/testes")
def criar_teste(mensagem: str):
    with SessionLocal() as db:
        teste = Teste(mensagem=mensagem)
        db.add(teste)
        db.commit()
        return {"id": teste.id, "mensagem": teste.mensagem}


@app.get("/testes")
def listar_testes():
    with SessionLocal() as db:
        testes = db.query(Teste).all()
        return [{"id": t.id, "mensagem": t.mensagem} for t in testes]