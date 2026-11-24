from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Teste(Base):
    __tablename__ = "teste"

    id: Mapped[int] = mapped_column(primary_key=True)
    mensagem: Mapped[str]