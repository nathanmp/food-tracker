"""empty message

Revision ID: 552e09f75d09
Revises: a2303d888188
Create Date: 2019-04-02 09:16:41.700183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '552e09f75d09'
down_revision = 'a2303d888188'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('foodtype', schema=None) as batch_op:
        batch_op.drop_column('user_id')
        batch_op.drop_column('username')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('foodtype', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.INTEGER(), nullable=True))
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['uid'])
        batch_op.drop_column('uid')

    # ### end Alembic commands ###
