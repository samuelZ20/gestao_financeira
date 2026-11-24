from sqlalchemy.orm import Session

from app.models import Categoria

# Categorias que todo usuário ganha ao criar a conta (RF001, RN22)
CATEGORIAS_PADRAO = [
    ("Salário", "receita"),
    ("Outras receitas", "receita"),
    ("Alimentação", "despesa"),
    ("Mercado", "despesa"),
    ("Casa", "despesa"),
    ("Transporte", "despesa"),
    ("Saúde", "despesa"),
    ("Assinaturas", "despesa"),
    ("Outros", "despesa"),
]


def criar_categorias_padrao(db: Session, usuario_id: int) -> None:
    """Adiciona as categorias padrão do usuário. Quem chama faz o commit."""
    for nome, tipo in CATEGORIAS_PADRAO:
        db.add(Categoria(usuario_id=usuario_id, nome=nome, tipo=tipo, padrao=True))