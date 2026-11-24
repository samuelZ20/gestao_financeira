from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Tipo = Literal["receita", "despesa"]


class CategoriaEntrada(BaseModel):
    """Dados enviados pelo front ao cadastrar (RF006) ou alterar (RF008)."""

    model_config = ConfigDict(str_strip_whitespace=True)  # tira espaços do começo e do fim

    # Depois de tirar os espaços, "   " vira "" e é recusado pelo min_length
    nome: str = Field(min_length=1, max_length=50)
    tipo: Tipo


class CategoriaSaida(BaseModel):
    """Categoria devolvida pela API (RF007). O front de lançamentos usa id, nome e tipo."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    tipo: Tipo
    padrao: bool  # RN09: True para as categorias criadas no cadastro
