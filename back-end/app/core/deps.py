"""Dependências compartilhadas pelas rotas."""

# TEMPORÁRIO: até o login real (RF002) ficar pronto, todas as rotas usam o
# usuário de id 1 ("usuário fixo", conforme o ritmo combinado no GITFLOW.md).
# Quando o módulo de acesso (pessoa A) entregar o JWT, é só trocar o corpo
# desta função para ler o usuário do token. As rotas não precisam mudar.
USUARIO_FIXO_ID = 1


def get_usuario_atual_id() -> int:
    return USUARIO_FIXO_ID
