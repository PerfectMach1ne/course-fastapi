"""create posts table(?)

Revision ID: 30efb7d6a615
Revises: 
Create Date: 2023-04-19 10:59:03.776539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30efb7d6a615'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                             sa.Column('title', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
