"""PROVISÓRIO: dados mínimos para desenvolver antes do login (RF002) existir.

Cria o usuário de id 1 e algumas categorias, só se o banco estiver vazio.
Rode uma vez, depois de `alembic upgrade head`:  python -m app.core.seed_dev
Sai de cena quando o módulo de Acesso e o de Categorias estiverem prontos.
"""
from datetime import datetime

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models import Categoria, Usuario

CATEGORIAS_PADRAO = [
    ("Salário", "receita"),
    ("Outras receitas", "receita"),
    ("Alimentação", "despesa"),
    ("Transporte", "despesa"),
    ("Moradia", "despesa"),
    ("Lazer", "despesa"),
]


def criar_dados_de_desenvolvimento() -> None:
    with SessionLocal() as db:
        if db.scalar(select(Usuario.id).limit(1)) is not None:
            return
        usuario = Usuario(
            id=1,
            nome="Usuário de teste",
            email="teste@meubolso.local",
            senha_hash="sem-login-ainda",
            politica_aceita_em=datetime.now(),
        )
        db.add(usuario)
        db.flush()
        for nome, tipo in CATEGORIAS_PADRAO:
            db.add(Categoria(usuario_id=usuario.id, nome=nome, tipo=tipo, padrao=True))
        db.commit()


if __name__ == "__main__":
    criar_dados_de_desenvolvimento()
    print("Dados de desenvolvimento criados (ou já existiam).")
