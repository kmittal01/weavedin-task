"""Variants table created

Revision ID: b121f90e85bb
Revises: 7fda687ad172
Create Date: 2018-08-30 12:08:54.096406

"""
from alembic import op
import sqlalchemy as sa
import app

# revision identifiers, used by Alembic.
revision = 'b121f90e85bb'
down_revision = '7fda687ad172'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('variant',
    sa.Column('id', app.sqlalchemy_utils.GUID(), nullable=False),
    sa.Column('item_id', app.sqlalchemy_utils.GUID(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('selling_price', sa.Integer(), nullable=True),
    sa.Column('cost_price', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(length=255), nullable=True),
    sa.Column('cloth', sa.String(length=255), nullable=True),
    sa.Column('modified_by', app.sqlalchemy_utils.GUID(), nullable=True),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', app.sqlalchemy_utils.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('variant')
    # ### end Alembic commands ###