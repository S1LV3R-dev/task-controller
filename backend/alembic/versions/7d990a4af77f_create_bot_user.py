"""create_bot_user

Revision ID: 7d990a4af77f
Revises: 7813c0d0ca9f
Create Date: 2025-03-06 11:46:35.199047+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d990a4af77f'
down_revision: Union[str, None] = '7813c0d0ca9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "INSERT INTO users(id, username, email, password) VALUES (0, 'bot', 'bot@task_controller.com', 'no_pass')"
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM users WHERE id=0"
    )
