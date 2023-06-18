"""Create settings

Revision ID: 409f6edeeb5d
Revises: 
Create Date: 2023-04-02 18:02:50.953634

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = "409f6edeeb5d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "settings",
        sa.Column("name", sa.String(length=255), primary_key=True),
        sa.Column("value", sa.String(length=255), nullable=False),
    )
    op.execute(
        f"""
        INSERT INTO settings
        (name, value)
        VALUES
        ('transactions_uploaded_at', '{datetime.utcnow().isoformat()}')
    """
    )


def downgrade() -> None:
    op.drop_table("settings")
