"""Cria as tabelas conta_pagar e orcamento.

Revision ID: e91ad632f50c
Revises: abd87f7a1de8
"""

import sqlalchemy as sa
from alembic import op

revision = "e91ad632f50c"
down_revision = "abd87f7a1de8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "conta_pagar",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuario.id"), nullable=False),
        sa.Column("categoria_id", sa.Integer(), sa.ForeignKey("categoria.id"), nullable=False),
        sa.Column("descricao", sa.String(150), nullable=False),
        sa.Column("valor", sa.Numeric(12, 2), nullable=False),
        sa.Column("vencimento", sa.Date(), nullable=False),
        sa.Column("status", sa.String(8), server_default="pendente", nullable=False),
        sa.Column("lancamento_id", sa.Integer(), sa.ForeignKey("lancamento.id")),
        sa.CheckConstraint("length(trim(descricao)) > 0", name="ck_conta_pagar_descricao"),
        sa.CheckConstraint("valor > 0", name="ck_conta_pagar_valor"),
        sa.CheckConstraint(
            "status IN ('pendente', 'paga', 'atrasada')", name="ck_conta_pagar_status"
        ),
        sa.CheckConstraint(
            "(status = 'paga' AND lancamento_id IS NOT NULL) OR "
            "(status <> 'paga' AND lancamento_id IS NULL)",
            name="ck_conta_pagar_status_lancamento",
        ),
        sa.UniqueConstraint("lancamento_id", name="uq_conta_pagar_lancamento"),
    )
    op.create_index("ix_conta_pagar_usuario_id", "conta_pagar", ["usuario_id"])
    op.create_index("ix_conta_pagar_categoria_id", "conta_pagar", ["categoria_id"])

    op.create_table(
        "orcamento",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("usuario_id", sa.Integer(), sa.ForeignKey("usuario.id"), nullable=False),
        sa.Column("categoria_id", sa.Integer(), sa.ForeignKey("categoria.id"), nullable=False),
        sa.Column("mes", sa.SmallInteger(), nullable=False),
        sa.Column("ano", sa.SmallInteger(), nullable=False),
        sa.Column("valor_limite", sa.Numeric(12, 2), nullable=False),
        sa.CheckConstraint("mes BETWEEN 1 AND 12", name="ck_orcamento_mes"),
        sa.CheckConstraint("ano BETWEEN 1000 AND 9999", name="ck_orcamento_ano"),
        sa.CheckConstraint("valor_limite > 0", name="ck_orcamento_valor_limite"),
        sa.UniqueConstraint("categoria_id", "mes", "ano", name="uq_orcamento_categoria_periodo"),
    )
    op.create_index("ix_orcamento_usuario_id", "orcamento", ["usuario_id"])


def downgrade() -> None:
    op.drop_table("orcamento")
    op.drop_table("conta_pagar")
