from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import criar_token_acesso, gerar_hash_senha, verificar_senha
from app.models import Usuario
from app.modules.acesso.schemas import CadastroEntrada, LoginEntrada
from app.modules.categorias.service import criar_categorias_padrao

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
    db.flush()  # manda o INSERT ao banco (sem confirmar) para o usuario ganhar um id
    criar_categorias_padrao(db, usuario.id)
    db.commit()  # usuário e categorias são salvos juntos (NF005)
    db.refresh(usuario)  # busca de volta o id e a data_cadastro gerados pelo banco
    return usuario

def autenticar(db: Session, dados: LoginEntrada) -> str:
    """RF002: confere e-mail e senha e devolve o token de acesso."""
    usuario = db.scalar(select(Usuario).where(Usuario.email == dados.email.lower()))

    # Mesma mensagem para e-mail inexistente e senha errada (fluxo alternativo do RF002)
    if usuario is None or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    return criar_token_acesso(usuario.id)