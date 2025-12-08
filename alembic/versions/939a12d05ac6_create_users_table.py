"""create users table

Revision ID: 939a12d05ac6
Revises: 
Create Date: 2025-12-08 12:38:11.513062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '939a12d05ac6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_name', sa.String(20), nullable=False),
        sa.Column('password', sa.String(60), nullable=False),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('status', sa.Integer, default=0, index=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
