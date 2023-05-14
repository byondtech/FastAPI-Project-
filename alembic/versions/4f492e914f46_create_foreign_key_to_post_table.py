"""create foreign key to post table

Revision ID: 4f492e914f46
Revises: ccbf517a3cab
Create Date: 2023-05-11 19:39:28.164843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4f492e914f46'
down_revision = 'ccbf517a3cab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable= False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users", local_cols= ["owner_id"],
                          remote_cols=["id"],ondelete= "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name= 'posts')
    op.drop_column('posts','owner_id')
    pass
