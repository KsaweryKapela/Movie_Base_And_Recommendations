"""empty message

Revision ID: ebb4efbd2a5f
Revises: e01f51db1a4e
Create Date: 2022-08-05 12:27:19.872708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebb4efbd2a5f'
down_revision = 'e01f51db1a4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie_actors', sa.Column('user_movie_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'movie_actors', 'users_films', ['user_movie_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'movie_actors', type_='foreignkey')
    op.drop_column('movie_actors', 'user_movie_id')
    # ### end Alembic commands ###