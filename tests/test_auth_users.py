from fastapi.testclient import TestClient

from app.core.security import hash_password
from app.domain.enums.user_role import UserRole
from app.infrastructure.database.session import SessionLocal
from app.main import app
from app.models.user import User

client = TestClient(app)

ADMIN_EMAIL = "isa@gmail.com"
ADMIN_PASSWORD = "SuperAdmin2026Segura"


def crear_super_admin():
    db = SessionLocal()
    try:
        db.add(
            User(
                first_name="Isaura",
                last_name="Suarez",
                email=ADMIN_EMAIL,
                password_hash=hash_password(ADMIN_PASSWORD),
                role=UserRole.SUPER_ADMIN,
                is_active=True,
            )
        )
        db.commit()
    finally:
        db.close()


def login(email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def auth(token):
    return {"Authorization": f"Bearer {token}"}


ESTETICISTA = {
    "first_name": "Laura",
    "last_name": "Gomez",
    "email": "laura@harmonyspa.com",
    "phone": "3001234567",
    "password": "LauraSpa2026Segura",
    "role": "ESTETICISTA",
    "employee_profile": {"job_title": "Esteticista", "specialty": "Tratamientos faciales"},
}

CLIENTE = {
    "first_name": "Maria",
    "last_name": "Rodriguez",
    "email": "maria@harmonyspa.com",
    "password": "MariaCliente2026Segura",
    "role": "CLIENTE",
    "client_profile": {"birth_date": "1990-05-15", "address": "Bogota"},
}


def test_login_me_logout_flow():
    crear_super_admin()

    response = login()
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert response.json()["expires_in"] == 7200

    me = client.get("/api/v1/auth/me", headers=auth(token))
    assert me.status_code == 200
    assert me.json()["role"] == "SUPER_ADMIN"
    assert "password_hash" not in me.json()

    assert client.post("/api/v1/auth/logout", headers=auth(token)).status_code == 204
    assert client.get("/api/v1/auth/me", headers=auth(token)).status_code == 401


def test_login_wrong_password_and_no_token():
    crear_super_admin()
    assert login(password="otra-clave-incorrecta").status_code == 401
    assert client.get("/api/v1/auth/me").status_code == 401


def test_super_admin_manages_users():
    crear_super_admin()
    token = login().json()["access_token"]
    headers = auth(token)

    created = client.post("/api/v1/users", json=ESTETICISTA, headers=headers)
    assert created.status_code == 201
    assert created.json()["role"] == "ESTETICISTA"
    assert "password" not in created.json() and "password_hash" not in created.json()

    assert client.post("/api/v1/users", json=CLIENTE, headers=headers).status_code == 201
    assert client.post("/api/v1/users", json=ESTETICISTA, headers=headers).status_code == 409

    listed = client.get("/api/v1/users?role=ESTETICISTA&is_active=true", headers=headers)
    assert listed.status_code == 200
    assert [u["email"] for u in listed.json()] == ["laura@harmonyspa.com"]

    user_id = created.json()["id"]
    assert client.get(f"/api/v1/users/{user_id}", headers=headers).status_code == 200
    assert client.get("/api/v1/users/9999", headers=headers).status_code == 404

    patched = client.patch(f"/api/v1/users/{user_id}", json={"phone": "3110000000"}, headers=headers)
    assert patched.status_code == 200
    assert patched.json()["phone"] == "3110000000"

    # El rol no se puede cambiar con una actualización ordinaria.
    client.patch(f"/api/v1/users/{user_id}", json={"role": "ADMIN"}, headers=headers)
    assert client.get(f"/api/v1/users/{user_id}", headers=headers).json()["role"] == "ESTETICISTA"


def test_validation_rules():
    crear_super_admin()
    headers = auth(login().json()["access_token"])

    segundo_super = {**ESTETICISTA, "role": "SUPER_ADMIN"}
    assert client.post("/api/v1/users", json=segundo_super, headers=headers).status_code == 422

    clave_corta = {**ESTETICISTA, "password": "corta"}
    assert client.post("/api/v1/users", json=clave_corta, headers=headers).status_code == 422

    cliente_sin_perfil = {k: v for k, v in CLIENTE.items() if k != "client_profile"}
    assert client.post("/api/v1/users", json=cliente_sin_perfil, headers=headers).status_code == 422

    perfil_cruzado = {**ESTETICISTA, "client_profile": CLIENTE["client_profile"]}
    assert client.post("/api/v1/users", json=perfil_cruzado, headers=headers).status_code == 422


def test_only_super_admin_can_manage_users():
    crear_super_admin()
    headers = auth(login().json()["access_token"])
    client.post("/api/v1/users", json=ESTETICISTA, headers=headers)

    token_laura = login("laura@harmonyspa.com", ESTETICISTA["password"]).json()["access_token"]
    assert client.get("/api/v1/users", headers=auth(token_laura)).status_code == 403
    assert client.get("/api/v1/users").status_code == 401


def test_deactivating_user_revokes_sessions():
    crear_super_admin()
    headers = auth(login().json()["access_token"])
    laura = client.post("/api/v1/users", json=ESTETICISTA, headers=headers).json()

    token_laura = login("laura@harmonyspa.com", ESTETICISTA["password"]).json()["access_token"]
    assert client.get("/api/v1/auth/me", headers=auth(token_laura)).status_code == 200

    off = client.patch(f"/api/v1/users/{laura['id']}/status", json={"is_active": False}, headers=headers)
    assert off.status_code == 200 and off.json()["is_active"] is False

    assert client.get("/api/v1/auth/me", headers=auth(token_laura)).status_code == 401
    assert login("laura@harmonyspa.com", ESTETICISTA["password"]).status_code == 401

    client.patch(f"/api/v1/users/{laura['id']}/status", json={"is_active": True}, headers=headers)
    assert login("laura@harmonyspa.com", ESTETICISTA["password"]).status_code == 200


def test_super_admin_cannot_deactivate_self():
    crear_super_admin()
    headers = auth(login().json()["access_token"])
    me = client.get("/api/v1/auth/me", headers=headers).json()
    response = client.patch(f"/api/v1/users/{me['id']}/status", json={"is_active": False}, headers=headers)
    assert response.status_code == 400
