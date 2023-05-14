"""add remaining columns to posts

Revision ID: 0b8ef53ddb5b
Revises: 4f492e914f46
Create Date: 2023-05-11 19:44:46.403136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b8ef53ddb5b'
down_revision = '4f492e914f46'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('posts') as batch_op:
        batch_op.add_column(sa.Column('content', sa.String(), nullable=False))
        batch_op.add_column(sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
        batch_op.add_column(sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    with op.batch_alter_table('posts') as batch_op:
        batch_op.drop_column('content')
        batch_op.drop_column('published')
        batch_op.drop_column('created_at')
    pass
