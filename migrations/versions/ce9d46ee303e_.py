"""empty message

Revision ID: ce9d46ee303e
Revises: 2d6bedb39d34
Create Date: 2019-04-03 09:13:48.749855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce9d46ee303e'
down_revision = '2d6bedb39d34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ts_created', sa.Integer(), nullable=True))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.INTEGER(), nullable=True))
        batch_op.drop_column('ts_created')

    # ### end Alembic commands ###
