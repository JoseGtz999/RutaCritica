"""Agregar columna tiempoReal a subtareas

Revision ID: cf8f6d3017c7
Revises: 8c41e045a0ee
Create Date: 2024-11-28 13:25:40.047219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf8f6d3017c7'
down_revision: Union[str, None] = '8c41e045a0ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subtareas', sa.Column('tiempoReal', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subtareas', 'tiempoReal')
    # ### end Alembic commands ###