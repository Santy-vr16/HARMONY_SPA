<p align="center">
  <pre align="center">
  ██╗  ██╗██████╗ ██████╗ ███╗   ██╗██████╗ ███╗   ██╗██╗   ██╗    ███████╗██████╗  █████╗ 
  ██║  ██║██╔══██╗██╔══██╗████╗  ██║██╔══██╗████╗  ██║╚██╗ ██╔╝    ██╔════╝██╔══██╗██╔══██╗
  ███████║███████║██████╔╝██╔██╗ ██║██║  ██║██╔██╗ ██║ ╚████╔╝     ███████╗██████╔╝███████║
  ██╔══██║██╔══██║██╔══██╗██║╚██╗██║██║  ██║██║╚██╗██║  ╚██╔╝      ╚════██║██╔═══╝ ██╔══██║
  ██║  ██║██║  ██║██║  ██║██║ ╚████║██████╔╝██║ ╚████║   ██║       ███████║██║     ██║  ██║
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═══╝   ╚═╝       ╚══════╝╚═╝     ╚═╝  ╚═╝
  </pre>
</p>

<h3 align="center">💅 REST API & BEAUTY MANAGEMENT SYSTEM 💆‍♀️</h3>

<p align="center">
  <a href="#-system-overview">
    <img src="https://img.shields.io/badge/EXPLORE-HARMONY_SPA-ff69b4?style=for-the-badge" alt="Explore">
  </a>
  <a href="#-architecture">
    <img src="https://img.shields.io/badge/ARCHITECTURE-SYSTEM-purple?style=for-the-badge" alt="Architecture">
  </a>
  <a href="#-getting-started">
    <img src="https://img.shields.io/badge/GET-STARTED-lightgrey?style=for-the-badge" alt="Get Started">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SENA_ADSO-FICHA_3315796-green?style=for-the-badge" alt="SENA">
  <img src="https://img.shields.io/badge/STATUS-IN_DEVELOPMENT-orange?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/PROJECT-BEAUTY_SPA-ff1493?style=for-the-badge" alt="Project">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy">
  <img src="https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white" alt="VS Code">
</p>

---

## 🌸 SYSTEM OVERVIEW

<p align="center">
  <i>Plataforma inteligente para la gestión de servicios de belleza, estética y relajación.</i>
</p>

**HARMONY SPA** es un sistema backend desarrollado para la gestión integral de spas y centros de estética corporal. Proporciona una solución robusta para:

* 📅 **Agendamiento y Citas:** Control de horarios para masajes, faciales y tratamientos estéticos.
* 💆‍♀️ **Catálogo de Servicios:** Administración de tarifas, tiempos y categorías de bienestar.
* 👥 **Gestión de Clientes y Terapeutas:** Asignación de especialistas y seguimiento de historial.
* 💾 **Persistencia Relacional:** Conexión segura y optimizada con MySQL mediante SQLAlchemy.

---

## 🏛️ ARCHITECTURE

El proyecto está diseñado bajo **Clean Architecture** (Arquitectura Limpia):

```text
Backend_SPA/
├── 📂 app/
│   ├── 📂 api/
│   │   ├── 📂 v1/
│   │   │   └── 📜 router.py
│   │   └── 📜 health.py
│   ├── 📂 core/
│   │   └── 📜 config.py
│   ├── 📂 domain/
│   ├── 📂 infrastructure/
│   │   └── 📂 database/
│   │       ├── 📜 connection.py
│   │       └── 📜 session.py
│   ├── 📂 models/
│   ├── 📂 repositories/
│   ├── 📂 schemas/
│   ├── 📂 services/
│   └── 📜 main.py
├── 📜 .env
├── 📜 README.md
└── 📜 requirements.txt


---

## 🚀 PUESTA EN MARCHA

```bash
# 1. Entorno virtual e instalación
python -m venv venv
source venv/Scripts/activate        # Git Bash en Windows (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt

# 2. Configuración: copia .env.example a .env y edita DATABASE_URL y JWT_SECRET_KEY
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"   # pega el resultado en JWT_SECRET_KEY

# 3. Base de datos (MySQL): crea la base una sola vez
#    CREATE DATABASE harmony_spa CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
alembic upgrade head

# 4. Crear el SUPER_ADMIN (una sola vez)
python -m scripts.create_super_admin

# 5. Iniciar la API  ->  http://127.0.0.1:8000/docs
uvicorn app.main:app --reload

# 6. Pruebas automáticas (usan SQLite temporal, no tocan MySQL)
python -m pytest -v
```

### Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/auth/login` | Iniciar sesión (devuelve JWT) |
| GET | `/api/v1/auth/me` | Perfil del usuario autenticado |
| POST | `/api/v1/auth/logout` | Cerrar la sesión actual |
| POST | `/api/v1/users` | Crear usuario (solo SUPER_ADMIN) |
| GET | `/api/v1/users` | Listar usuarios (`?role=&is_active=&skip=&limit=`) |
| GET | `/api/v1/users/{id}` | Consultar usuario |
| PATCH | `/api/v1/users/{id}` | Actualizar datos |
| PATCH | `/api/v1/users/{id}/status` | Activar / desactivar (revoca sesiones al desactivar) |
