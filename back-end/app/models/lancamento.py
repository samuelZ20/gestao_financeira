from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Lancamento(Base):
    """Entrada (receita) ou saída (despesa) de dinheiro."""

    __tablename__ = "lancamento"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), index=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"))
    tipo: Mapped[str] = mapped_column(String(7))  # "receita" ou "despesa"
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    data: Mapped[date] = mapped_column(default=date.today)
    descricao: Mapped[str] = mapped_column(String(150))

    categoria = relationship("Categoria")
