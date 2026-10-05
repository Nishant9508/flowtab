import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, get_db
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.drop_all(bind=test_engine)
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_generate_demo():
    response = client.post("/api/v1/demo/generate", json={"account_id": "test-acct", "region": "eu-west-1"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Check if DB was populated
    db = TestingSessionLocal()
    from app.models import FlowtabSource
    src = db.query(FlowtabSource).first()
    assert src.account_id == "test-acct"
    assert src.region == "eu-west-1"
    db.close()
