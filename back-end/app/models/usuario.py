from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Usuario(Base):
    """Pessoa que usa o sistema. Campos conforme o dicionário de dados (tabela usuario)."""

    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True)  # RN01: e-mail único
    senha_hash: Mapped[str] = mapped_column(String(255))  # RN16: só o hash bcrypt
    politica_aceita_em: Mapped[datetime] = mapped_column(DateTime)  # RN15
    data_cadastro: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())