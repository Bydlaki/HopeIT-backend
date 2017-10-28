"""empty message

Revision ID: dfeb429998ff
Revises: 
Create Date: 2017-10-28 01:56:47.898184

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfeb429998ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('device', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('goal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('target', sa.Integer(), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('finish_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('notify_freq', sa.Enum('week', 'month', name='notificationsfreq'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goal')
    op.drop_table('user')
    # ### end Alembic commands ###