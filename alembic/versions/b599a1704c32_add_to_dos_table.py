"""add to_dos table

Revision ID: b599a1704c32
Revises: 939a12d05ac6
Create Date: 2025-12-08 16:06:40.673572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b599a1704c32'
down_revision: Union[str, Sequence[str], None] = '939a12d05ac6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("to_dos",
        sa.Column("id", sa.Integer, primary_key= True),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("status", sa.Integer, default=0, nullable=False),
        sa.Column("created_by", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default= sa.func.now(), nullable=False),
        sa.Column("updated_by", sa.Integer, nullable=False),
        sa.Column("updated_at", sa.DateTime, nullable=True)
    )


def downgrade() -> None:
  op.drop_table("to_dos")
