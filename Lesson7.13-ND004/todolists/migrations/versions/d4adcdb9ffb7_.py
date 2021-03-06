"""empty message

Revision ID: d4adcdb9ffb7
Revises: 9af03232d1aa
Create Date: 2021-06-23 22:20:46.591002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4adcdb9ffb7'
down_revision = '9af03232d1aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###

    # manual update to set 'completed' field to false for all existing data
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')

    # manual update to change 'completed' field SET to NOT NULLABLE
    op.alter_column('todos', 'completed', nullable=False)



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
