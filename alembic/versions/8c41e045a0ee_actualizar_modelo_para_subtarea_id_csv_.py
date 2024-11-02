"""Actualizar modelo para subtarea_id_csv como String

Revision ID: 8c41e045a0ee
Revises: bc4fd043af44
Create Date: 2024-11-19 21:25:33.347142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c41e045a0ee'
down_revision: Union[str, None] = 'bc4fd043af44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subtareas', 'subtarea_id_csv',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subtareas', 'subtarea_id_csv',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    # ### end Alembic commands ###