"""cria tabelas categoria (provisória) e lancamento

Revision ID: 7d41b8e5c2a9
Revises: 2c600e88d0b3
Create Date: 2026-11-23 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d41b8e5c2a9'
down_revision: Union[str, Sequence[str], None] = '2c600e88d0b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # categoria: versão mínima, só para a chave estrangeira de lancamento.
    # Quem fizer o módulo Categorias (RF006 a RF009) completa o model e
    # gera uma nova migração com o que faltar (ex.: único por usuário e tipo).
    op.create_table('categoria',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=50), nullable=False),
    sa.Column('tipo', sa.String(length=7), nullable=False),
    sa.Column('padrao', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lancamento',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('categoria_id', sa.Integer(), nullable=False),
    sa.Column('tipo', sa.String(length=7), nullable=False),
    sa.Column('valor', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('data', sa.Date(), nullable=False),
    sa.Column('descricao', sa.String(length=150), nullable=False),
    sa.ForeignKeyConstraint(['categoria_id'], ['categoria.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lancamento_usuario_id'), 'lancamento', ['usuario_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_lancamento_usuario_id'), table_name='lancamento')
    op.drop_table('lancamento')
    op.drop_table('categoria')
