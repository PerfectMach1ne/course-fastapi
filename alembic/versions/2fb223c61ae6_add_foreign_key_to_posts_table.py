"""add foreign key to posts table

Revision ID: 2fb223c61ae6
Revises: b7385a02a747
Create Date: 2023-04-19 11:38:19.879184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fb223c61ae6'
down_revision = 'b7385a02a747'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('_fk_posts_users', source_table="posts", referent_table="users",
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('_fk_posts_users', table_name="posts")
    op.drop_column('posts', 'owner_id')
