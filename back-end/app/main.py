from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.acesso.router import router as acesso_router

app = FastAPI(title="Meu Bolso API")

# Deixa o front-end (porta 5173) chamar esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(acesso_router)


@app.get("/hello")
def hello():
    return {"mensagem": "Olá do Meu Bolso!"}