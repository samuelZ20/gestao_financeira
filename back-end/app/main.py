from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.categorias.router import router as categorias_router
from app.modules.lancamentos.router import router as lancamentos_router
from app.modules.lancamentos.router import tratar_erro_de_regra
from app.modules.lancamentos.service import RegraDeNegocioError

app = FastAPI(title="Meu Bolso API")
app.add_exception_handler(RegraDeNegocioError, tratar_erro_de_regra)
app.include_router(categorias_router)
app.include_router(lancamentos_router)

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
