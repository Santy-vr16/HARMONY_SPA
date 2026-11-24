"""crear perfiles de cliente y empleado

Revision ID: a1f3c9d27b54
Revises: 6e748feebc9c
Create Date: 2026-11-22 10:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "a1f3c9d27b54"
down_revision = "6e748feebc9c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "client_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("address", sa.String(255), nullable=True),
        sa.Column("emergency_contact_name", sa.String(150), nullable=True),
        sa.Column("emergency_contact_phone", sa.String(30), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_client_profiles_user_id"),
    )

    op.create_table(
        "employee_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("job_title", sa.String(100), nullable=False),
        sa.Column("specialty", sa.String(150), nullable=True),
        sa.Column("hire_date", sa.Date(), nullable=True),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", name="uq_employee_profiles_user_id"),
    )


def downgrade() -> None:
    op.drop_table("employee_profiles")
    op.drop_table("client_profiles")
