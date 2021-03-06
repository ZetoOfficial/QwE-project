"""init

Revision ID: e6c280bd7e83
Revises: 
Create Date: 2022-07-02 00:09:08.971898

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = 'e6c280bd7e83'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('area', sa.String(), nullable=True),
    sa.Column('salary', sa.Integer(), nullable=True),
    sa.Column('experience', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('key_skills', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('alternate_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancy')
    op.drop_table('area')
    # ### end Alembic commands ###
