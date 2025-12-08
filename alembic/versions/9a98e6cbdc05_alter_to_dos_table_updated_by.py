"""alter to_dos table updated_by 

Revision ID: 9a98e6cbdc05
Revises: a9a9a2c7d05b
Create Date: 2025-12-08 16:38:05.784874

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a98e6cbdc05'
down_revision: Union[str, Sequence[str], None] = 'a9a9a2c7d05b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "to_dos",
        "updated_by",
        existing_type=sa.Integer(),
        nullable=True
    )



def downgrade() -> None:
   op.alter_column(
        "to_dos",
        "updated_by",
        existing_type=sa.Integer(),
        nullable=False
   )
