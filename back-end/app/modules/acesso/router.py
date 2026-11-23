from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.acesso import service
from app.modules.acesso.schemas import CadastroEntrada, LoginEntrada, TokenResposta, UsuarioResposta

router = APIRouter(prefix="/acesso", tags=["Acesso"])


@router.post("/cadastro", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def cadastrar(dados: CadastroEntrada, db: Session = Depends(get_db)):
    """RF001 - Criar conta."""
    return service.criar_usuario(db, dados)

@router.post("/login", response_model=TokenResposta)
def entrar(dados: LoginEntrada, db: Session = Depends(get_db)):
    """RF002 - Entrar no sistema."""
    token = service.autenticar(db, dados)
    return TokenResposta(access_token=token)