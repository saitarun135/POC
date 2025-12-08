"""add user_todos_link table

Revision ID: a9a9a2c7d05b
Revises: b599a1704c32
Create Date: 2025-12-08 16:12:55.901843

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9a9a2c7d05b'
down_revision: Union[str, Sequence[str], None] = 'b599a1704c32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user_todos_link",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, index=True, nullable=False),
        sa.Column("todo_id", sa.Integer, index=True, nullable=False),
        sa.Column("status", sa.Integer, default=0, nullable=False, index=True)
    )


def downgrade() -> None:
   op.drop_table("user_todos_link")
