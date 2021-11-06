"""add tag

Revision ID: 37c7d4304634
Revises: 054969ff6ed7
Create Date: 2021-11-06 21:04:14.138869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37c7d4304634'
down_revision = '054969ff6ed7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_tag'))
    )
    op.create_table('tags_to_posts',
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name=op.f('fk_tags_to_posts_post_id_post')),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_tags_to_posts_tag_id_tag'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags_to_posts')
    op.drop_table('tag')
    # ### end Alembic commands ###
