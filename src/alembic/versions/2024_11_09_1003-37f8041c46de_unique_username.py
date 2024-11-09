"""unique username

Revision ID: 37f8041c46de
Revises: 9e483584c4f9
Create Date: 2024-11-09 10:03:32.682857

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "37f8041c46de"
down_revision: Union[str, None] = "9e483584c4f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        op.f("uq_users_username"), "users", ["username"]
    )


def downgrade() -> None:
    op.drop_constraint(op.f("uq_users_username"), "users", type_="unique")
