"""Dependências compartilhadas pelas rotas."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import ler_token_acesso
from app.models import Usuario

# Lê o cabeçalho "Authorization: Bearer <token>" de cada requisição.
# auto_error=False: quando falta o token, quem responde é a nossa função,
# com a nossa mensagem, e não o FastAPI.
esquema_bearer = HTTPBearer(auto_error=False)


def get_usuario_atual_id(
    credenciais: Annotated[HTTPAuthorizationCredentials | None, Depends(esquema_bearer)],
    db: Annotated[Session, Depends(get_db)],
) -> int:
    """RN17 e RN18: devolve o id do usuário dono do token ou recusa a requisição."""
    usuario_id = ler_token_acesso(credenciais.credentials) if credenciais else None

    # Token ausente, inválido, vencido ou de um usuário que já não existe
    if usuario_id is None or db.get(Usuario, usuario_id) is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Faça login para continuar.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario_id