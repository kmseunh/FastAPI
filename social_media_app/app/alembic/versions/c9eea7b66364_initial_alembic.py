"""Initial alembic..

Revision ID: c9eea7b66364
Revises: f4d99962c780
Create Date: 2024-04-09 00:35:56.680276

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c9eea7b66364"
down_revision: Union[str, None] = "f4d99962c780"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("followers_count", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("followings_count", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "followings_count")
    op.drop_column("users", "followers_count")
    # ### end Alembic commands ###