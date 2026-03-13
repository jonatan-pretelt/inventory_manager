import os
import urllib.parse
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.main import app
from app.database import Base, get_db
from fastapi.testclient import TestClient

username = os.environ.get("POSTGRES_SUPERUSER")
password = os.environ.get("POSTGRES_SUPERPW")
encoded_password = urllib.parse.quote_plus(str(password)) #Escaping Special Characters such as @ signs in Passwords
host = "localhost"
port="5432"
db = "inventory_db_test"


TEST_DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}:{port}/{db}"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(setup_database):
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture()
def client(db_session: Session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

