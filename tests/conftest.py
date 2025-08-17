from app.main import app
from app.database import get_db, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest
from app.oauth2 import create_access_token


# can be hardcoded because it's a testing db
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)


@pytest.fixture
def session(): #scope="module"
    # print("\n i wiped the database and resterted it")
    Base.metadata.drop_all(bind=engine) # if test fails with pytest -x, the tables remain
    Base.metadata.create_all(bind=engine)  # create testing db tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session): #now each test has access to the database as well as the client
    # print("\ni made a new testing database session")
    def override_get_db():
        db = TestingSessionLocal()
        try:
           yield session
        finally:
           db.close()
    
    app.dependency_overrides[get_db] = override_get_db  ### det_db = TestingSessionLocal()
    yield TestClient(app) # code can run both before and after the test runs


@pytest.fixture
def test_user(client):
    # print("\ni created a test client")
    user_data = {"email":"slender@man.gg","password":"forget-me-not"}
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client
