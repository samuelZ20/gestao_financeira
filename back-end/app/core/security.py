import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env

# Configurações do token (NF011), lidas do .env
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha em hash bcrypt (RN16). Não tem como desfazer."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Confere se a senha digitada gera o mesmo hash salvo (usada no login, RF002)."""
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))


def criar_token_acesso(usuario_id: int) -> str:
    """Gera o crachá (JWT) do usuário, válido por ACCESS_TOKEN_EXPIRE_MINUTES (NF011)."""
    expira_em = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados = {"sub": str(usuario_id), "exp": expira_em}
    return jwt.encode(dados, SECRET_KEY, algorithm=JWT_ALGORITHM)


def ler_token_acesso(token: str) -> int | None:
    """Confere a assinatura e a validade do token. Devolve o id do usuário ou None."""
    try:
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "sub"]},
        )
    except jwt.InvalidTokenError:  # assinatura errada, token vencido ou incompleto
        return None
    return int(dados["sub"])