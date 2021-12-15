"""subject add remark canceled

Revision ID: a2477458abf0
Revises: 
Create Date: 2021-12-15 09:40:33.800505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2477458abf0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subject', sa.Column('canceled', sa.Integer(), nullable=True))
    op.add_column('subject', sa.Column('remark', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subject', 'remark')
    op.drop_column('subject', 'canceled')
    # ### end Alembic commands ###
