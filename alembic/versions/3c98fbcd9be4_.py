"""empty message

Revision ID: 3c98fbcd9be4
Revises: dd5de15f2a80
Create Date: 2017-10-27 20:43:31.433432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c98fbcd9be4'
down_revision = 'dd5de15f2a80'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('finish_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('notify_freq', sa.Enum('week', 'month', name='notificationsfreq'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goal')
    # ### end Alembic commands ###