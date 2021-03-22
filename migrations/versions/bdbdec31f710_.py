"""empty message

Revision ID: bdbdec31f710
Revises: 491771c2e008
Create Date: 2021-03-22 14:01:51.018366

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdbdec31f710'
down_revision = '491771c2e008'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('nb_char', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'nb_char')
    # ### end Alembic commands ###