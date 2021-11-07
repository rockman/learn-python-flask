"""uuid to user

Revision ID: eb68e72fe7d5
Revises: 37c7d4304634
Create Date: 2021-11-07 11:50:42.768463

"""
from alembic import op
import sqlalchemy as sa

from uuid import uuid4


# revision identifiers, used by Alembic.
revision = 'eb68e72fe7d5'
down_revision = '37c7d4304634'
branch_labels = None
depends_on = None


Base = sa.orm.declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.Text, nullable=False)
    uuid = sa.Column(sa.String(64), nullable=False, default=lambda: str(uuid4()))

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.String(length=64), nullable=True))

    session = sa.orm.Session(bind=op.get_bind())

    for user in session.query(User).all():
        user.uuid = str(uuid4())
        session.add(user)
    session.commit()

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('uuid', nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('uuid')

    # ### end Alembic commands ###