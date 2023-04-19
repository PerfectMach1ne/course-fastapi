"""add content column to posts table

Revision ID: 71ffd7835bc3
Revises: 30efb7d6a615
Create Date: 2023-04-19 11:15:37.516815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71ffd7835bc3'
down_revision = '30efb7d6a615'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
