from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Orcamento(Base):
    """Limite mensal de despesa de uma categoria."""

    __tablename__ = "orcamento"
    __table_args__ = (
        CheckConstraint("mes BETWEEN 1 AND 12", name="ck_orcamento_mes"),
        CheckConstraint("ano BETWEEN 1000 AND 9999", name="ck_orcamento_ano"),
        CheckConstraint("valor_limite > 0", name="ck_orcamento_valor_limite"),
        UniqueConstraint("categoria_id", "mes", "ano", name="uq_orcamento_categoria_periodo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), index=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"))
    mes: Mapped[int] = mapped_column(SmallInteger, default=lambda: date.today().month)
    ano: Mapped[int] = mapped_column(SmallInteger, default=lambda: date.today().year)
    valor_limite: Mapped[Decimal] = mapped_column(Numeric(12, 2))
