"""empty message

Revision ID: 94623cc8e293
Revises: cb366fb58de1
Create Date: 2019-06-22 11:46:35.203358

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94623cc8e293'
down_revision = 'cb366fb58de1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('weightelement')
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.add_column(sa.Column('weightval', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('meal', schema=None) as batch_op:
        batch_op.drop_column('weightval')

    op.create_table('weightelement',
    sa.Column('ts_created', sa.INTEGER(), nullable=True),
    sa.Column('uid', sa.VARCHAR(length=64), nullable=True),
    sa.Column('val', sa.FLOAT(), nullable=True),
    sa.Column('mealid', sa.INTEGER(), nullable=True),
    sa.Column('weightid', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['mealid'], ['meal.mid'], name='fk_weightelement'),
    sa.ForeignKeyConstraint(['uid'], ['user.username'], )
    )
    # ### end Alembic commands ###