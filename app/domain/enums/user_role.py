"""Roles de usuario de Harmony Spa."""

import enum


class UserRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    ESTETICISTA = "ESTETICISTA"
    CLIENTE = "CLIENTE"
