"""empty message

Revision ID: 79b932374ddd
Revises: 100021c4d14c
Create Date: 2019-06-19 11:01:16.061244

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79b932374ddd'
down_revision = '100021c4d14c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exerciseelement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('previous_changes', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exerciseelement', schema=None) as batch_op:
        batch_op.drop_column('previous_changes')
        batch_op.drop_column('active')

    # ### end Alembic commands ###
