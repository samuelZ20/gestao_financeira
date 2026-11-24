from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_usuario_atual_id
from app.modules.lancamentos import service
from app.modules.lancamentos.schemas import (
    ExtratoSaida,
    LancamentoEntrada,
    LancamentoSaida,
)

router = APIRouter(prefix="/lancamentos", tags=["Lançamentos"])

Db = Annotated[Session, Depends(get_db)]
UsuarioId = Annotated[int, Depends(get_usuario_atual_id)]


def _saida(db: Session, lancamento) -> LancamentoSaida:
    saida = LancamentoSaida.model_validate(lancamento)
    saida.gerado_por_conta = service.gerado_por_conta(db, lancamento.id)
    return saida


@router.post("", response_model=LancamentoSaida, status_code=201)
def registrar_lancamento(dados: LancamentoEntrada, db: Db, usuario_id: UsuarioId):
    """RF010 - Registrar lançamento."""
    return _saida(db, service.registrar(db, usuario_id, dados))


@router.get("", response_model=ExtratoSaida)
def consultar_lancamentos(
    db: Db,
    usuario_id: UsuarioId,
    ano: int = Query(default_factory=lambda: date.today().year, ge=2000, le=2100),
    mes: int = Query(default_factory=lambda: date.today().month, ge=1, le=12),
    tipo: str | None = Query(default=None, pattern="^(receita|despesa)$"),
    categoria_id: int | None = None,
):
    """RF011 - Consultar lançamentos do mês (padrão: mês corrente)."""
    itens, saldo = service.consultar_mes(db, usuario_id, ano, mes, tipo, categoria_id)
    return ExtratoSaida(
        itens=[_saida(db, i) for i in itens],
        quantidade=len(itens),
        saldo_periodo=saldo,
    )


@router.put("/{lancamento_id}", response_model=LancamentoSaida)
def alterar_lancamento(
    lancamento_id: int, dados: LancamentoEntrada, db: Db, usuario_id: UsuarioId
):
    """RF012 - Alterar lançamento."""
    return _saida(db, service.alterar(db, usuario_id, lancamento_id, dados))


@router.delete("/{lancamento_id}", status_code=204)
def excluir_lancamento(lancamento_id: int, db: Db, usuario_id: UsuarioId):
    """RF013 - Excluir lançamento."""
    service.excluir(db, usuario_id, lancamento_id)
    return Response(status_code=204)


def tratar_erro_de_regra(_request, erro: service.RegraDeNegocioError):
    """Transforma o erro de regra de negócio em JSON: {detail, campo}."""
    return JSONResponse(
        status_code=erro.status,
        content={"detail": erro.mensagem, "campo": erro.campo},
    )
