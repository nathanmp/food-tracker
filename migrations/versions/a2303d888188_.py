"""empty message

Revision ID: a2303d888188
Revises: 555ff9266c67
Create Date: 2019-04-02 09:10:12.589152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2303d888188'
down_revision = '555ff9266c67'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('foodtype', sa.Column('user_id', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'foodtype', type_='foreignkey')
    op.create_foreign_key(None, 'foodtype', 'user', ['user_id'], ['uid'])
    op.drop_column('foodtype', 'username')
    # ### end Alembic commands ###
