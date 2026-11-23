from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Tipo = Literal["receita", "despesa"]


class LancamentoEntrada(BaseModel):
    """Dados enviados pelo front ao registrar (RF010) ou alterar (RF012)."""

    tipo: Tipo
    descricao: str = Field(max_length=150)
    valor: Decimal = Field(gt=0, max_digits=12, decimal_places=2)  # RN02
    data: date = Field(default_factory=date.today)
    categoria_id: int

    @field_validator("descricao")
    @classmethod
    def descricao_obrigatoria(cls, texto: str) -> str:
        texto = texto.strip()
        if not texto:
            raise ValueError("A descrição é obrigatória.")  # RN23
        return texto


class CategoriaResumo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str


class LancamentoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo: Tipo
    descricao: str
    valor: Decimal
    data: date
    categoria: CategoriaResumo
    gerado_por_conta: bool = False  # True: só a conta a pagar altera (RN10)


class ExtratoSaida(BaseModel):
    """Resposta da consulta do mês (RF011)."""

    itens: list[LancamentoSaida]
    quantidade: int
    saldo_periodo: Decimal  # receitas - despesas do que está filtrado (RN03)
