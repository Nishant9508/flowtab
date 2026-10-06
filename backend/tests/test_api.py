import pytest
from fastapi.testclient import TestClient
import re
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

@pytest.fixture(scope="module", autouse=True)
def generate_data():
    client.post("/api/v1/demo/generate", json={})

def test_api_summary_and_docs_match():
    # Read the DOCS
    with open("../docs/DEMO_STORIES.md") as f:
        docs = f.read()

    # Extract dollars
    s3_val = float(re.search(r"S3 over NAT approx: \$([0-9.]+)", docs).group(1))
    chatty_val = float(re.search(r"Chatty app cross AZ: \$([0-9.]+)", docs).group(1))
    peer_val = float(re.search(r"Replication peering: \$([0-9.]+)", docs).group(1))
    alb_val = float(re.search(r"ALB true outbound.*: \$([0-9.]+)", docs).group(1))
    spike_val = float(re.search(r"Spike Day 6: \$([0-9.]+)", docs).group(1))
    
    summary = client.get("/api/v1/network/summary").json()
    cats = summary["by_category"]
    
    assert abs(cats["NAT Gateway Data Processing"] - s3_val) < 0.1
    assert abs(cats["Inter-AZ Data Transfer"] - chatty_val) < 0.1
    assert abs(cats["Inter-Region Data Transfer"] - peer_val) < 0.1
    assert abs(cats["Internet Egress"] - (alb_val + spike_val)) < 15.0 # within $15 due to unbilled estimation lag

    # Check shape
    assert "daily_series" in summary
    assert len(summary["daily_series"]) == 8 # Spans 7-8 distinct days depending on UTC hours generated
    assert "hourly" in summary["daily_series"][0]

def test_api_findings_dynamic():
    data = client.get("/api/v1/network/findings").json()
    assert data["status"] == "success"
    titles = [f["title"] for f in data["findings"]]
    # Should dynamically detect the spikes and S3
    assert any("S3 Traffic via NAT Gateway" in t for t in titles)
    assert any("High Inter-AZ Communication" in t for t in titles)
    assert any("Cross-Region Database Replication" in t for t in titles)
    assert any("Spike in Internet Egress" in t for t in titles)
    assert any("ALB True-Outbound Correction" in t for t in titles)

def test_api_charges():
    data = client.get("/api/v1/network/charges").json()
    assert data["status"] == "success"
    items = data["data"]
    assert len(items) > 0
    s3_charge = next(i for i in items if i["charge_category"] == "NAT Gateway Data Processing")
    assert s3_charge["share_of_total"] > 0.50 # roughly 58%
    assert s3_charge["share_of_total"] < 0.65 

def test_api_flow_graph():
    data = client.get("/api/v1/network/flow-graph").json()
    nodes = data["data"]["nodes"]
    links = data["data"]["links"]
    assert len(nodes) > 0
    assert len(links) > 0
    assert "usd" in links[0]

def test_api_architecture():
    data = client.get("/api/v1/network/architecture").json()
    accounts = data["data"]["accounts"]
    assert len(accounts) == 2 # We seeded 111111111111 and 222222222222
    assert "regions" in accounts[0]
    
def test_api_reconciliation():
    data = client.get("/api/v1/network/reconciliation").json()
    assert len(data["data"]) > 0
    internet = next(c for c in data["data"] if c["charge_category"] == "Internet Egress")
    assert internet["status"] == "corrected"
    assert internet["difference_percent"] > 0
    assert internet["waiting_for_bill_usd"] > 0

def test_api_summary_filters_and_sums():
    # Fetch without filters
    res_all = client.get("/api/v1/network/summary").json()
    
    # Fetch with vpc filter
    res_filt = client.get("/api/v1/network/summary?vpc_id=vpc-a1").json()
    assert res_filt["total_usd"] < res_all["total_usd"]
    
    # Fetch flows
    flows = client.get("/api/v1/network/flows?vpc_id=vpc-a1").json()
    sum_usd = sum(f["usd"] for f in flows["data"])
    assert abs(res_filt["total_usd"] - sum_usd) < 2.0

def test_api_estimated_status():
    db = TestingSessionLocal()
    from app.models import FlowRecord
    estimated_count = db.query(FlowRecord).filter(FlowRecord.is_estimated == True).count()
    assert estimated_count == 24 # 6 hours * 4 flows/hr = 24 (spike isn't in last 6 hrs)
    db.close()
    
def test_setup_checks():
    res = client.get("/api/v1/network/setup/checks").json()
    assert res["data"]["flow_logs"] == True
    assert res["data"]["cur"] == True
    assert "stub" not in res["data"]
