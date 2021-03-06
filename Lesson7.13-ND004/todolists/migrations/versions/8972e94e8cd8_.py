"""empty message

Revision ID: 8972e94e8cd8
Revises: c58187c851fd
Create Date: 2021-06-25 18:57:53.584997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8972e94e8cd8'
down_revision = 'c58187c851fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
