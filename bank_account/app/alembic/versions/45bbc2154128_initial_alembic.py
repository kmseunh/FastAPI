"""Initial alembic..

Revision ID: 45bbc2154128
Revises: 6ecbb21db714
Create Date: 2024-04-03 11:39:47.373517

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45bbc2154128'
down_revision: Union[str, None] = '6ecbb21db714'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_number', sa.String(), nullable=True),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_account_number'), 'accounts', ['account_number'], unique=True)
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_account_number'), table_name='accounts')
    op.drop_table('accounts')
    # ### end Alembic commands ###
