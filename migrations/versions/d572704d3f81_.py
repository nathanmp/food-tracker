"""empty message

Revision ID: d572704d3f81
Revises: f85a7a43ad7a
Create Date: 2019-04-28 12:48:01.717245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd572704d3f81'
down_revision = 'f85a7a43ad7a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posttags',
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('tid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pid'], ['post.pid'], ),
    sa.ForeignKeyConstraint(['tid'], ['tag.tid'], ),
    sa.PrimaryKeyConstraint('pid', 'tid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posttags')
    # ### end Alembic commands ###
