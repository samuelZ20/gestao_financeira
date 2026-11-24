from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Desejo(Base):
    """Meta de compra do usuário (dicionário de dados: desejo). Usada na Sprint 3 (RF021 a RF024)."""

    __tablename__ = "desejo"
    __table_args__ = (
        CheckConstraint("valor > 0", name="ck_desejo_valor"),  # RN29
        CheckConstraint("length(trim(nome)) > 0", name="ck_desejo_nome"),  # nome não vazio
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), index=True)
    nome: Mapped[str] = mapped_column(String(100))
    descricao: Mapped[str | None] = mapped_column(String(200))  # opcional
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2))