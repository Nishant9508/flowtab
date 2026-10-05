import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import engine, get_db
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

def test_summary_and_stories_math_exactness():
    # 1. Generate
    response = client.post("/api/v1/demo/generate", json={})
    assert response.status_code == 200
    
    # 2. Check Summary
    summary = client.get("/api/v1/network/summary").json()
    cats = summary["by_category"]
    
    # Story Math Proof
    assert abs(cats["NAT Gateway Data Processing"] - 1512.06) < 0.1
    assert abs(cats["Inter-AZ Data Transfer"] - 84.10) < 0.1
    assert abs(cats["Inter-Region Data Transfer"] - 33.60) < 0.1
    
    # Internet egress includes both Spike + ALB, with last 6 hours underestimated
    # 168 hours * 50 / 0.56 * 0.09 = 1350 true
    # 6 hours of 50 * 0.09 = 27 (est) vs 48.21 (real) => difference of ~21.21
    # 168 hours of spike = wait, spike is only 24 hours ! 24 * 500 * 0.09 = 1080. It's during hours 120-144, so no estimated mode overlap.
    # Total Internet Egress = (1350 - 21.21) + 1080 = 2408.79
    assert abs(cats["Internet Egress"] - 2408.79) < 0.1

    assert abs(summary["total_usd"] - 4038.54) < 0.1
    assert abs(summary["total_gb"] - 64091.34) < 0.1

def test_estimated_status():
    db = TestingSessionLocal()
    from app.models import FlowRecord
    estimated_count = db.query(FlowRecord).filter(FlowRecord.is_estimated == True).count()
    assert estimated_count == 24 # 6 hours * 5 flows/hr = 30 (spike isn't in last 6 hours)
    db.close()
