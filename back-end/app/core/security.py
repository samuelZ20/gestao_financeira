import bcrypt


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha em hash bcrypt (RN16). Não tem como desfazer."""
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Confere se a senha digitada gera o mesmo hash salvo (usada no login, RF002)."""
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))