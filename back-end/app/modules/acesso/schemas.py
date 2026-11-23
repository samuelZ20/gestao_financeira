from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class CadastroEntrada(BaseModel):
    """Dados que o front-end envia na tela I_Cadastro (RF001)."""

    model_config = ConfigDict(str_strip_whitespace=True)  # tira espaços do começo e do fim

    nome: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(max_length=150)
    senha: str = Field(min_length=8)  # RN16: mínimo de 8 caracteres
    aceita_politica: bool  # RN15

    @field_validator("senha")
    @classmethod
    def senha_cabe_no_bcrypt(cls, senha: str) -> str:
        """O bcrypt só aceita até 72 bytes (letras com acento ocupam 2)."""
        if len(senha.encode("utf-8")) > 72:
            raise ValueError("A senha é longa demais.")
        return senha

    @field_validator("aceita_politica")
    @classmethod
    def politica_deve_ser_aceita(cls, aceitou: bool) -> bool:
        """RN15: sem o aceite da política de privacidade, não há cadastro."""
        if not aceitou:
            raise ValueError("É preciso aceitar a política de privacidade.")
        return aceitou


class UsuarioResposta(BaseModel):
    """O que a API devolve sobre o usuário. Nunca inclui a senha nem o hash."""

    model_config = ConfigDict(from_attributes=True)  # permite montar a partir do model Usuario

    id: int
    nome: str
    email: str