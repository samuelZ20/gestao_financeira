"""Configuração dos testes: banco SQLite em memória, sem precisar do Docker."""
import os
import sys
from datetime import datetime
from pathlib import Path

# Precisa vir antes de importar a aplicação (o database.py lê a variável).
os.environ["DATABASE_URL"] = "sqlite://"
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "back-end"))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models import Categoria, Usuario
from app.core.deps import get_usuario_atual_id


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    sessao = sessionmaker(bind=engine)()
    agora = datetime.now()
    sessao.add_all(
        [
            Usuario(id=1, nome="Ana", email="ana@x.com", senha_hash="h", politica_aceita_em=agora),
            Usuario(id=2, nome="Beto", email="beto@x.com", senha_hash="h", politica_aceita_em=agora),
            Categoria(id=1, usuario_id=1, nome="Salário", tipo="receita"),
            Categoria(id=2, usuario_id=1, nome="Alimentação", tipo="despesa"),
            Categoria(id=3, usuario_id=1, nome="Lazer", tipo="despesa"),
            Categoria(id=4, usuario_id=2, nome="Alimentação", tipo="despesa"),
        ]
    )
    sessao.commit()
    yield sessao
    sessao.close()
    Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    # Os testes de lançamentos rodam como o usuário 1, sem precisar fazer login
    app.dependency_overrides[get_usuario_atual_id] = lambda: 1
    yield TestClient(app)
    app.dependency_overrides.clear()
