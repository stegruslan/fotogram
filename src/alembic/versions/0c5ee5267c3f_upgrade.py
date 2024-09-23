"""upgrade

Revision ID: 0c5ee5267c3f
Revises: ed98fc81241b
Create Date: 2024-09-21 22:09:41.217764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c5ee5267c3f'
down_revision: Union[str, None] = 'ed98fc81241b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
