"""add last few columns to posts table

Revision ID: a6a186b3458e
Revises: 2fb223c61ae6
Create Date: 2023-04-19 11:44:26.865703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6a186b3458e'
down_revision = '2fb223c61ae6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False,
                                     server_default=sa.text('NOW()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
