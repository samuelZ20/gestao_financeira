from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import gerar_hash_senha
from app.models import Usuario
from app.modules.acesso.schemas import CadastroEntrada


def criar_usuario(db: Session, dados: CadastroEntrada) -> Usuario:
    """RF001: cadastra um usuário novo, com a senha guardada só como hash."""
    email = dados.email.lower()  # "Ana@Gmail.com" e "ana@gmail.com" são o mesmo e-mail

    # RN01: o e-mail é único
    ja_existe = db.scalar(select(Usuario).where(Usuario.email == email))
    if ja_existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este e-mail já está cadastrado.",
        )

    usuario = Usuario(
        nome=dados.nome,
        email=email,
        senha_hash=gerar_hash_senha(dados.senha),  # RN16
        politica_aceita_em=datetime.now(),  # RN15: guarda quando aceitou
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)  # busca de volta o id e a data_cadastro gerados pelo banco
    return usuario