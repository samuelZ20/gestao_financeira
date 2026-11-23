"""PROVISÓRIO: só a listagem, que o formulário de lançamento precisa.

A pessoa A (módulo Categorias) implementa o CRUD completo (RF006 a RF009)
e substitui este arquivo.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_usuario_atual_id
from app.models import Categoria

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("")
def listar_categorias(
    db: Annotated[Session, Depends(get_db)],
    usuario_id: Annotated[int, Depends(get_usuario_atual_id)],
    tipo: str | None = Query(default=None, pattern="^(receita|despesa)$"),
):
    consulta = select(Categoria).where(Categoria.usuario_id == usuario_id)
    if tipo:
        consulta = consulta.where(Categoria.tipo == tipo)
    categorias = db.scalars(consulta.order_by(Categoria.nome))
    return [{"id": c.id, "nome": c.nome, "tipo": c.tipo} for c in categorias]
