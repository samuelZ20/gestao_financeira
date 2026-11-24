"""Regras de negócio das categorias (RF006 a RF009)."""
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import Base
from app.models import Categoria, Lancamento
from app.modules.categorias.schemas import CategoriaEntrada
from app.modules.lancamentos.service import RegraDeNegocioError

# Categorias que todo usuário ganha ao criar a conta (RF001, RN22)
CATEGORIAS_PADRAO = [
    ("Salário", "receita"),
    ("Outras receitas", "receita"),
    ("Alimentação", "despesa"),
    ("Mercado", "despesa"),
    ("Casa", "despesa"),
    ("Transporte", "despesa"),
    ("Saúde", "despesa"),
    ("Assinaturas", "despesa"),
    ("Outros", "despesa"),
]

MSG_NOME_DUPLICADO = "Você já tem uma categoria com esse nome."  # IE_CategoriaDuplicada


def criar_categorias_padrao(db: Session, usuario_id: int) -> None:
    """Adiciona as categorias padrão do usuário. Quem chama faz o commit."""
    for nome, tipo in CATEGORIAS_PADRAO:
        db.add(Categoria(usuario_id=usuario_id, nome=nome, tipo=tipo, padrao=True))


def listar(db: Session, usuario_id: int, tipo: str | None = None) -> list[Categoria]:
    """RF007: lista as categorias do usuário (RN18), em ordem de nome.

    Se o tipo vier ("receita" ou "despesa"), traz só as daquele tipo.
    """
    consulta = select(Categoria).where(Categoria.usuario_id == usuario_id)
    if tipo:
        consulta = consulta.where(Categoria.tipo == tipo)
    return list(db.scalars(consulta.order_by(Categoria.nome)))


def _buscar_do_usuario(db: Session, usuario_id: int, categoria_id: int) -> Categoria:
    """RN18: só enxerga categoria do próprio usuário.

    Categoria de outro usuário responde igual a uma que não existe,
    para não revelar que ela existe.
    """
    categoria = db.scalar(
        select(Categoria).where(
            Categoria.id == categoria_id, Categoria.usuario_id == usuario_id
        )
    )
    if categoria is None:
        raise RegraDeNegocioError("Categoria não encontrada.", 404)
    return categoria


def _garantir_nome_disponivel(
    db: Session,
    usuario_id: int,
    nome: str,
    tipo: str,
    ignorar_id: int | None = None,
) -> None:
    """RN21: o nome é único por usuário e tipo, sem diferenciar maiúsculas.

    ignorar_id: ao alterar, a própria categoria não conta como repetida.
    """
    consulta = select(Categoria.id).where(
        Categoria.usuario_id == usuario_id,
        Categoria.tipo == tipo,
        func.lower(Categoria.nome) == nome.lower(),
    )
    if ignorar_id is not None:
        consulta = consulta.where(Categoria.id != ignorar_id)
    if db.scalar(consulta) is not None:
        raise RegraDeNegocioError(MSG_NOME_DUPLICADO, 409, "nome")


def _bloquear_padrao(categoria: Categoria) -> None:
    """RN09: as categorias padrão não podem ser alteradas nem excluídas."""
    if categoria.padrao:
        raise RegraDeNegocioError(
            "Categorias padrão não podem ser alteradas nem excluídas.", 403
        )


def _esta_em_uso(db: Session, categoria_id: int) -> bool:
    """RN04 e RN14: a categoria já tem lançamentos ou contas a pagar?

    A tabela conta_pagar é da pessoa C. Enquanto o modelo dela não existir
    (ou não tiver a coluna categoria_id), só os lançamentos contam.
    """
    tem_lancamento = db.scalar(
        select(Lancamento.id).where(Lancamento.categoria_id == categoria_id)
    )
    if tem_lancamento is not None:
        return True

    conta_pagar = Base.metadata.tables.get("conta_pagar")
    if conta_pagar is None or "categoria_id" not in conta_pagar.c:
        return False
    tem_conta = db.scalar(
        select(conta_pagar.c.id).where(conta_pagar.c.categoria_id == categoria_id)
    )
    return tem_conta is not None


def _salvar(db: Session, categoria: Categoria) -> Categoria:
    """Faz o commit. Se o banco recusar pelo índice único da RN21, desfaz e avisa.

    Acontece quando duas requisições iguais chegam ao mesmo tempo: as duas
    passam por _garantir_nome_disponivel, mas o banco só aceita a primeira.
    """
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise RegraDeNegocioError(MSG_NOME_DUPLICADO, 409, "nome")
    db.refresh(categoria)
    return categoria


def cadastrar(db: Session, usuario_id: int, dados: CategoriaEntrada) -> Categoria:
    """RF006: cria uma categoria do usuário (nunca padrão)."""
    _garantir_nome_disponivel(db, usuario_id, dados.nome, dados.tipo)  # RN21

    categoria = Categoria(
        usuario_id=usuario_id, nome=dados.nome, tipo=dados.tipo, padrao=False
    )
    db.add(categoria)
    return _salvar(db, categoria)


def alterar(
    db: Session, usuario_id: int, categoria_id: int, dados: CategoriaEntrada
) -> Categoria:
    """RF008: muda o nome e/ou o tipo de uma categoria do usuário."""
    categoria = _buscar_do_usuario(db, usuario_id, categoria_id)
    _bloquear_padrao(categoria)  # RN09
    _garantir_nome_disponivel(  # RN21
        db, usuario_id, dados.nome, dados.tipo, ignorar_id=categoria.id
    )

    # RN14: mudar o tipo deixaria lançamentos e contas com categoria do tipo errado
    if dados.tipo != categoria.tipo and _esta_em_uso(db, categoria.id):
        raise RegraDeNegocioError(
            "O tipo não pode ser alterado porque a categoria já tem lançamentos ou contas.",
            409,
            "tipo",
        )

    categoria.nome = dados.nome
    categoria.tipo = dados.tipo
    return _salvar(db, categoria)


def excluir(db: Session, usuario_id: int, categoria_id: int) -> None:
    """RF009: exclui uma categoria que o usuário criou e não usou."""
    categoria = _buscar_do_usuario(db, usuario_id, categoria_id)
    _bloquear_padrao(categoria)  # RN09
    if _esta_em_uso(db, categoria.id):  # RN04
        raise RegraDeNegocioError(
            "Esta categoria já tem lançamentos ou contas e não pode ser excluída.", 409
        )

    # Os limites de orçamento da categoria saem junto, na mesma transação.
    # A tabela orcamento ainda não existe; quando existir, passa a valer.
    orcamento = Base.metadata.tables.get("orcamento")
    if orcamento is not None and "categoria_id" in orcamento.c:
        db.execute(delete(orcamento).where(orcamento.c.categoria_id == categoria.id))

    db.delete(categoria)
    db.commit()
