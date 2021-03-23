"""Changed name of Todo model

Revision ID: e2d84dc92cc6
Revises: e7336410a36a
Create Date: 2021-03-23 14:53:22.374268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2d84dc92cc6'
down_revision = 'e7336410a36a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_created'), 'task', ['created'], unique=False)
    op.create_index(op.f('ix_task_modified'), 'task', ['modified'], unique=False)
    op.drop_index('ix_todo_created', table_name='todo')
    op.drop_index('ix_todo_modified', table_name='todo')
    op.drop_table('todo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), nullable=True),
    sa.Column('status', sa.VARCHAR(length=50), nullable=True),
    sa.Column('created', sa.DATETIME(), nullable=True),
    sa.Column('modified', sa.DATETIME(), nullable=True),
    sa.Column('category', sa.VARCHAR(length=50), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_todo_modified', 'todo', ['modified'], unique=False)
    op.create_index('ix_todo_created', 'todo', ['created'], unique=False)
    op.drop_index(op.f('ix_task_modified'), table_name='task')
    op.drop_index(op.f('ix_task_created'), table_name='task')
    op.drop_table('task')
    # ### end Alembic commands ###