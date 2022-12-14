"""str to int

Revision ID: 0b951a992f6e
Revises: 3d44b5213f94
Create Date: 2022-07-21 02:53:50.686513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b951a992f6e'
down_revision = '3d44b5213f94'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies_database', sa.Column('computed_audience_score', sa.Integer(), nullable=True))
    op.add_column('movies_database', sa.Column('computed_critic_score', sa.Integer(), nullable=True))
    op.add_column('users_films', sa.Column('computed_audience_score', sa.Integer(), nullable=True))
    op.add_column('users_films', sa.Column('computed_critic_score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_films', 'computed_critic_score')
    op.drop_column('users_films', 'computed_audience_score')
    op.drop_column('movies_database', 'computed_critic_score')
    op.drop_column('movies_database', 'computed_audience_score')
    # ### end Alembic commands ###
