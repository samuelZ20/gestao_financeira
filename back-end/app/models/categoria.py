from sqlalchemy import ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Categoria(Base):
    """Agrupa lançamentos, contas a pagar e orçamentos (dicionário de dados: categoria)."""

    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    nome: Mapped[str] = mapped_column(String(50))
    tipo: Mapped[str] = mapped_column(String(7))  # "receita" ou "despesa"
    padrao: Mapped[bool] = mapped_column(default=False)  # RN09: criada no cadastro

    __table_args__ = (
        # RN21: nome único por usuário e tipo, sem diferenciar maiúsculas e minúsculas
        Index(
            "uq_categoria_usuario_tipo_nome",
            "usuario_id",
            "tipo",
            func.lower(nome),
            unique=True,
        ),
    )