from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_usuario_atual_id
from app.modules.categorias import service
from app.modules.categorias.schemas import CategoriaEntrada, CategoriaSaida

router = APIRouter(prefix="/categorias", tags=["Categorias"])

Db = Annotated[Session, Depends(get_db)]
UsuarioId = Annotated[int, Depends(get_usuario_atual_id)]


@router.get("", response_model=list[CategoriaSaida])
def listar_categorias(
    db: Db,
    usuario_id: UsuarioId,
    tipo: str | None = Query(default=None, pattern="^(receita|despesa)$"),
):
    """RF007 - Consultar categorias (filtro opcional por tipo)."""
    return service.listar(db, usuario_id, tipo)


@router.post("", response_model=CategoriaSaida, status_code=201)
def cadastrar_categoria(dados: CategoriaEntrada, db: Db, usuario_id: UsuarioId):
    """RF006 - Cadastrar categoria."""
    return service.cadastrar(db, usuario_id, dados)


@router.put("/{categoria_id}", response_model=CategoriaSaida)
def alterar_categoria(
    categoria_id: int, dados: CategoriaEntrada, db: Db, usuario_id: UsuarioId
):
    """RF008 - Alterar categoria."""
    return service.alterar(db, usuario_id, categoria_id, dados)


@router.delete("/{categoria_id}", status_code=204)
def excluir_categoria(categoria_id: int, db: Db, usuario_id: UsuarioId):
    """RF009 - Excluir categoria."""
    service.excluir(db, usuario_id, categoria_id)
    return Response(status_code=204)
