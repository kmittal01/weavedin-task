"""initial migration

Revision ID: 7fda687ad172
Revises: 
Create Date: 2018-08-30 11:14:28.205940

"""
import app
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fda687ad172'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('item',
    sa.Column('id', app.sqlalchemy_utils.GUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('brand', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('product_code', sa.String(length=255), nullable=True),
    sa.Column('modified_by', app.sqlalchemy_utils.GUID(), nullable=True),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', app.sqlalchemy_utils.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', app.sqlalchemy_utils.GUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password', sa.String(length=256), nullable=True),
    sa.Column('modified_by', app.sqlalchemy_utils.GUID(), nullable=True),
    sa.Column('modified_on', sa.DateTime(), nullable=True),
    sa.Column('created_by', app.sqlalchemy_utils.GUID(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('item')
    # ### end Alembic commands ###