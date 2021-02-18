import os
import sys

sys.path.append(os.getcwd())
sys.path.append("{}/app".format(os.getcwd()))

from app.fastapi_main import app
from database import Base
from fastapi.testclient import TestClient
from fastapi_main import app, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def helper_clear_wine_table(db: Session = TestingSessionLocal()):
    # clears the wine table for testing purposes
    db.execute("""DELETE FROM wine""")
    db.commit()
    db.close()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_items():
    response = client.get("/items/1", params={"q": "first item description"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "q": "first item description"}


def test_get_sklearn_wine():
    response = client.get("/sklearn_wine")
    assert response.status_code == 200
    assert len(response.json()) == 178


def test_get_sqlite_wine():
    helper_clear_wine_table()

    response = client.get("/sqlite_wine")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


def test_post_sqlite_wine():
    helper_clear_wine_table()

    data = client.get("/sklearn_wine")
    assert data.status_code == 200
    assert len(data.json()) == 178

    response = client.post("/sqlite_wine", json=data.json())
    assert response.status_code == 200
    assert response.json()["processed"] == 178
