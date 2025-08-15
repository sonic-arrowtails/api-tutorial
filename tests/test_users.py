from fastapi.testclient import TestClient
from app.main import app
from app import schemas

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "change change change chasnge"
    assert res.status_code == 200

def test_create_user():
    res =  client.post("/users/", json={"email":"slender@man.gg","password":"forget-me-not"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "slender@man.gg"
    assert res.status_code == 201