""" b4652afdbacc, New Migration

Revision ID: d3a0fab5dda5
Revises: b4652afdbacc
Create Date: 2022-04-28 02:28:20.214506

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3a0fab5dda5'
down_revision = 'b4652afdbacc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'customer', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'customer', type_='unique')
    # ### end Alembic commands ###
