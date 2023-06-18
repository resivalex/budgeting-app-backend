"""Create dumps

Revision ID: e36a2316e146
Revises: 409f6edeeb5d
Create Date: 2023-04-02 19:53:09.552940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e36a2316e146"
down_revision = "409f6edeeb5d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dumps",
        sa.Column("uploaded_at", sa.DateTime, primary_key=True, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dumps")
