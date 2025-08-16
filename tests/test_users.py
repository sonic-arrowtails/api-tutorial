from app import schemas
from .database import client, session
import pytest
from jose import jwt
from app.config import settings

@pytest.fixture
def test_user(client):
    # print("\ni created a test client")
    user_data = {"email":"slender@man.gg","password":"forget-me-not"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

def test_root(client):
    res = client.get("/")
    # print(res.json())
    assert res.json().get("message") == "change change change chasnge"
    assert res.status_code == 200


def test_create_user(client):  # no trailing / in path leads to 307 redirect intstead of 201
    res = client.post("/users/", json={"email":"slender@man.gg","password":"forget-me-not"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "slender@man.gg"
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login", data={"username":test_user["email"],"password":test_user["password"]})

    assert res.status_code == 200

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id : str = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
