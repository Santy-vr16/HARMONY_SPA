"""Importar todos los modelos aquí permite que Alembic y SQLAlchemy los registren."""

from app.models.base import Base
from app.models.client_profile import ClientProfile
from app.models.employee_profile import EmployeeProfile
from app.models.user import User
from app.models.user_session import UserSession

__all__ = ["Base", "ClientProfile", "EmployeeProfile", "User", "UserSession"]
