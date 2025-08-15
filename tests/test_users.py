from fastapi.testclient import TestClient
from app import schemas
from app.main import app
from app.database import get_db, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest


# can be hardcoded because it's a testing db
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)




def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client(): 
    Base.metadata.drop_all(bind=engine) # if test fails with pytest -x, the tables remain
    Base.metadata.create_all(bind=engine)  # create testing db tables

    # import alembic command,
    # command.upgrade("head")
    # command.downgrade("base")

    yield TestClient(app) # code can run both before and after the test runs


def test_root(client):
    res = client.get("/")
    print(res.json())
    assert res.json().get("message") == "change change change chasnge"
    assert res.status_code == 200

def test_create_user(client):
    res =  client.post("/users/", json={"email":"slender@man.gg","password":"forget-me-not"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "slender@man.gg"
    assert res.status_code == 201
