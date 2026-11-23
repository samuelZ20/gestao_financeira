"""Regras de negócio dos lançamentos (RF010 a RF013)."""
from calendar import monthrange
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models import Categoria, Lancamento
from app.modules.lancamentos.schemas import LancamentoEntrada

MSG_GERADO_POR_CONTA = (
    "Este lançamento foi gerado por uma conta a pagar. "
    "Altere pela tela de Contas a pagar."
)


class RegraDeNegocioError(Exception):
    """Erro de regra de negócio. O router converte em resposta HTTP."""

    def __init__(self, mensagem: str, status: int = 422, campo: str | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.status = status
        self.campo = campo


def _buscar_categoria(db: Session, usuario_id: int, categoria_id: int) -> Categoria:
    categoria = db.scalar(
        select(Categoria).where(
            Categoria.id == categoria_id, Categoria.usuario_id == usuario_id
        )
    )
    if categoria is None:
        raise RegraDeNegocioError("Categoria não encontrada.", 422, "categoria_id")
    return categoria


def _validar_categoria_do_tipo(categoria: Categoria, tipo: str) -> None:
    """RN02: despesa usa categoria de despesa, receita usa categoria de receita."""
    if categoria.tipo != tipo:
        raise RegraDeNegocioError(
            f"A categoria escolhida não é do tipo {tipo}.", 422, "categoria_id"
        )


def gerado_por_conta(db: Session, lancamento_id: int) -> bool:
    """RN10: o lançamento foi criado ao pagar uma conta a pagar?

    A tabela conta_pagar é da pessoa C. Enquanto o modelo dela não existir,
    nenhum lançamento pode ter sido gerado por conta.
    """
    conta_pagar = Base.metadata.tables.get("conta_pagar")
    if conta_pagar is None:
        return False
    achou = db.scalar(
        select(conta_pagar.c.id).where(conta_pagar.c.lancamento_id == lancamento_id)
    )
    return achou is not None


def _buscar_do_usuario(db: Session, usuario_id: int, lancamento_id: int) -> Lancamento:
    """RN18: só enxerga lançamento do próprio usuário."""
    lancamento = db.scalar(
        select(Lancamento).where(
            Lancamento.id == lancamento_id, Lancamento.usuario_id == usuario_id
        )
    )
    if lancamento is None:
        raise RegraDeNegocioError("Lançamento não encontrado.", 404)
    return lancamento


def registrar(db: Session, usuario_id: int, dados: LancamentoEntrada) -> Lancamento:
    """RF010: registra uma receita ou despesa."""
    categoria = _buscar_categoria(db, usuario_id, dados.categoria_id)
    _validar_categoria_do_tipo(categoria, dados.tipo)

    lancamento = Lancamento(usuario_id=usuario_id, **dados.model_dump())
    db.add(lancamento)
    db.commit()
    db.refresh(lancamento)
    return lancamento


def consultar_mes(
    db: Session,
    usuario_id: int,
    ano: int,
    mes: int,
    tipo: str | None = None,
    categoria_id: int | None = None,
) -> tuple[list[Lancamento], Decimal]:
    """RF011: lista os lançamentos do mês (mais recente primeiro) e o saldo."""
    inicio = date(ano, mes, 1)
    fim = date(ano, mes, monthrange(ano, mes)[1])

    consulta = select(Lancamento).where(
        Lancamento.usuario_id == usuario_id,
        Lancamento.data >= inicio,
        Lancamento.data <= fim,
    )
    if tipo:
        consulta = consulta.where(Lancamento.tipo == tipo)
    if categoria_id:
        consulta = consulta.where(Lancamento.categoria_id == categoria_id)
    consulta = consulta.order_by(Lancamento.data.desc(), Lancamento.id.desc())

    itens = list(db.scalars(consulta))
    saldo = sum(
        (i.valor if i.tipo == "receita" else -i.valor for i in itens), Decimal("0")
    )
    return itens, saldo


def alterar(
    db: Session, usuario_id: int, lancamento_id: int, dados: LancamentoEntrada
) -> Lancamento:
    """RF012: corrige um lançamento."""
    lancamento = _buscar_do_usuario(db, usuario_id, lancamento_id)
    if gerado_por_conta(db, lancamento.id):
        raise RegraDeNegocioError(MSG_GERADO_POR_CONTA, 409)  # RN10

    categoria = _buscar_categoria(db, usuario_id, dados.categoria_id)
    _validar_categoria_do_tipo(categoria, dados.tipo)

    for campo, valor in dados.model_dump().items():
        setattr(lancamento, campo, valor)
    db.commit()
    db.refresh(lancamento)
    return lancamento


def excluir(db: Session, usuario_id: int, lancamento_id: int) -> None:
    """RF013: exclui um lançamento registrado por engano."""
    lancamento = _buscar_do_usuario(db, usuario_id, lancamento_id)
    if gerado_por_conta(db, lancamento.id):
        raise RegraDeNegocioError(MSG_GERADO_POR_CONTA, 409)  # RN10

    db.delete(lancamento)
    db.commit()
