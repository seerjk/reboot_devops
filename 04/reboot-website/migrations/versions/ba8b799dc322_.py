"""empty message

Revision ID: ba8b799dc322
Revises: d1ab73a1ed11
Create Date: 2016-06-05 14:03:32.514868

"""

# revision identifiers, used by Alembic.
revision = 'ba8b799dc322'
down_revision = 'd1ab73a1ed11'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('server', sa.Column('ipinfo', sa.String(length=250), nullable=True))
    op.drop_column('server', 'ipinfo1')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('server', sa.Column('ipinfo1', mysql.VARCHAR(length=250), nullable=True))
    op.drop_column('server', 'ipinfo')
    ### end Alembic commands ###
