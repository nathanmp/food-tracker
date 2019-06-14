"""empty message

Revision ID: a4a9fa4fe35d
Revises: f3629067b7fc
Create Date: 2019-06-14 09:12:10.432871

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4a9fa4fe35d'
down_revision = 'f3629067b7fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercisetype', schema=None) as batch_op:
        batch_op.add_column(sa.Column('etid', sa.Integer(), nullable=True))
        batch_op.create_foreign_key("exercisetype_id", 'user', ['etid'], ['uid'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercisetype', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('etid')

    # ### end Alembic commands ###