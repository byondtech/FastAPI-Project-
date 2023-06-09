"""Create Post Table

Revision ID: 7fa843a37632
Revises: 
Create Date: 2023-05-08 13:55:34.596469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fa843a37632'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column('id',sa.Integer(),nullable= False
                                       ,primary_key= True),sa.Column('title',sa.String(),nullable= False),
                                       sa.Column('content',sa.String(),nullable= False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
