from app import schemas
from app.config import settings
from jose import jwt

import pytest


def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == "Holi2!"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json = {
                "email": "user@example.com",
                "name": "User",
                "password": "password123"
            })
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "user@example.com"
    assert res.status_code == 201

def test_login_user(client, dummy_users):
    res = client.post("/login/", data = {
                "username": dummy_users[0]["email"],
                "password": dummy_users[0]["password"]
            })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == dummy_users[0]["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@example.com", "password123", 403),
    ("user@example.com", "wrongpassword", 403),
    ("wrongemail@example.com", "wrongpassword", 403),
    ("wrongemail@gmail.com", "password123", 403),
    (None, "password123", 422),
    ("user@example.com", None, 422)
])
def test_incorrect_login(client, dummy_users, email, password, status_code):
    res = client.post("/login/", data = {
                "username": email,
                "password": password
            })
    assert res.status_code == status_code

# pytest --disable-warnings -v -x