from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Categoria(Base):
    """PROVISÓRIO: versão mínima só para a chave estrangeira de lançamento.

    A pessoa A (módulo Categorias) substitui este arquivo pela versão final.
    """

    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    nome: Mapped[str] = mapped_column(String(50))
    tipo: Mapped[str] = mapped_column(String(7))  # "receita" ou "despesa"
    padrao: Mapped[bool] = mapped_column(default=False)
