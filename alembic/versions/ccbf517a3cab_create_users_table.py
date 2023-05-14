"""create Users table

Revision ID: ccbf517a3cab
Revises: 7fa843a37632
Create Date: 2023-05-10 11:35:57.900221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccbf517a3cab'
down_revision = '7fa843a37632'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id',sa.Integer,nullable= False),
                    sa.Column('email',sa.String,nullable= False),
                    sa.Column('password',sa.String,nullable= False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone= True),nullable= False,
                              server_default=sa.text('now()') ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
