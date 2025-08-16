from app.main import app
from app.database import get_db, Base
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
import pytest


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
