"""upgrade

Revision ID: 3e1712a6bda1
Revises: 0c5ee5267c3f
Create Date: 2024-09-21 22:50:22.702206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e1712a6bda1'
down_revision: Union[str, None] = '0c5ee5267c3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
