"""
Configuración de pruebas: usa una base SQLite temporal para NO tocar tu MySQL.
Las variables de entorno se definen antes de importar la aplicación.
"""

import os
import tempfile

_tmp_dir = tempfile.mkdtemp(prefix="harmony_tests_")
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp_dir}/test.db"
os.environ["JWT_SECRET_KEY"] = "clave-solo-para-pruebas-de-harmony-spa-1234567890"

import pytest  # noqa: E402

from app.infrastructure.database.connection import engine  # noqa: E402
from app.models import Base  # noqa: E402


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
