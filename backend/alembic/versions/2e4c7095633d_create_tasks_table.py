"""create_tasks_table

Revision ID: 2e4c7095633d
Revises: 7d990a4af77f
Create Date: 2025-03-06 13:15:46.969959+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e4c7095633d'
down_revision: Union[str, None] = '7d990a4af77f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.String(255)),
        sa.Column('status', sa.Integer, nullable=False, server_default="0"),
        sa.Column('deadline', sa.DateTime),
        sa.Column('created_by', sa.Integer, sa.ForeignKey('users.id'), nullable=False, server_default="0")
    )


def downgrade() -> None:
    op.drop_table('tasks')
