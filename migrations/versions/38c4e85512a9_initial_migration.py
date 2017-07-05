"""initial migration

Revision ID: 38c4e85512a9
Revises: None
Create Date: 2013-12-27 01:23:59.392801

"""

# revision identifiers, used by Alembic.
revision = '38c4e85512a9'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    role_table = op.create_table('role',
                                 sa.Column('id', sa.Integer(), nullable=False),
                                 sa.Column('name', sa.String(length=80),
                                           nullable=True),
                                 sa.Column('description', sa.String(length=255),
                                           nullable=True),
                                 sa.PrimaryKeyConstraint('id'),
                                 sa.UniqueConstraint('name'))

    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=64), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True, default=True),
        sa.PrimaryKeyConstraint('id'))
    op.create_index('ix_users_username', 'user', ['username'], unique=True)
    op.bulk_insert(
        role_table,
        [
            {"id": "1", "name": "admin", "description": "Administrator"},
            {"id": "2", "name": "mod", "description": "Moderator"},
            {"id": "3", "name": "user", "description": "Normal User"},
        ]
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_username', 'user')
    op.drop_table('user')
    ### end Alembic commands ###
