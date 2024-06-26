"""Initial alembic..

Revision ID: 7db1aa0dcf4b
Revises: df6674dba57b
Create Date: 2024-04-07 15:03:28.851119

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7db1aa0dcf4b'
down_revision: Union[str, None] = 'df6674dba57b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_dt', sa.DateTime(), nullable=True))
    op.drop_column('posts', 'created_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('posts', 'created_dt')
    # ### end Alembic commands ###
