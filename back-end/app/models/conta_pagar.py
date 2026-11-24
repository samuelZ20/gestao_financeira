from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ContaPagar(Base):
    """Conta com vencimento e vínculo com o lançamento gerado no pagamento."""

    __tablename__ = "conta_pagar"
    __table_args__ = (
        CheckConstraint("length(trim(descricao)) > 0", name="ck_conta_pagar_descricao"),
        CheckConstraint("valor > 0", name="ck_conta_pagar_valor"),
        CheckConstraint(
            "status IN ('pendente', 'paga', 'atrasada')", name="ck_conta_pagar_status"
        ),
        CheckConstraint(
            "(status = 'paga' AND lancamento_id IS NOT NULL) OR "
            "(status <> 'paga' AND lancamento_id IS NULL)",
            name="ck_conta_pagar_status_lancamento",
        ),
        UniqueConstraint("lancamento_id", name="uq_conta_pagar_lancamento"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), index=True)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categoria.id"), index=True)
    descricao: Mapped[str] = mapped_column(String(150))
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    vencimento: Mapped[date]
    status: Mapped[str] = mapped_column(String(8), server_default="pendente")
    lancamento_id: Mapped[int | None] = mapped_column(ForeignKey("lancamento.id"))
