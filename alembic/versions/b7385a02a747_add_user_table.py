"""add user table

Revision ID: b7385a02a747
Revises: 71ffd7835bc3
Create Date: 2023-04-19 11:27:36.152430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7385a02a747'
down_revision = '71ffd7835bc3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )


def downgrade() -> None:
    op.drop_table('users')
