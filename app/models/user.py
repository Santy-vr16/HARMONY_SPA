from datetime import datetime

from sqlalchemy import Boolean, Computed, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums.user_role import UserRole
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", native_enum=False, length=20),
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Columna generada: vale 1 solo para el SUPER_ADMIN y NULL para los demás.
    # Al ser UNIQUE, MySQL impide que exista más de un SUPER_ADMIN.
    super_admin_slot: Mapped[int | None] = mapped_column(
        Integer,
        Computed("CASE WHEN role = 'SUPER_ADMIN' THEN 1 ELSE NULL END", persisted=True),
        unique=True,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    sessions = relationship("UserSession", back_populates="user", passive_deletes=True)
    client_profile = relationship(
        "ClientProfile", back_populates="user", uselist=False, passive_deletes=True
    )
    employee_profile = relationship(
        "EmployeeProfile", back_populates="user", uselist=False, passive_deletes=True
    )
