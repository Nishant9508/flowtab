from datetime import datetime, timezone
import pytest
from app.models import BilledLine, FlowRecord
from app.network.bill import allocate_bill_to_flows
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

def test_allocate_bill_exact_match(db_session):
    hour = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    
    # Create mock flows totaling $1.00 estimated
    f1 = FlowRecord(hour=hour, vpc_id="vpc-1", charge_category="Egress", estimated_usd=0.25, is_estimated=True)
    f2 = FlowRecord(hour=hour, vpc_id="vpc-1", charge_category="Egress", estimated_usd=0.75, is_estimated=True)
    f3 = FlowRecord(hour=hour, vpc_id="vpc-1", charge_category="Intra", estimated_usd=0.00, is_estimated=True)
    db_session.add_all([f1, f2, f3])
    
    # Bill says it was actually $2.00
    b1 = BilledLine(hour=hour, usage_type="Egress", cost_usd=2.00)
    db_session.add(b1)
    db_session.commit()
    
    allocate_bill_to_flows(db_session, hour, "vpc-1")
    
    # Check if the $2 was split $0.50 and $1.50
    assert f1.billed_usd == 0.50
    assert f2.billed_usd == 1.50
    # Intra remained 0
    assert f3.billed_usd == 0.00
    
    assert f1.is_estimated == False
    assert f2.is_estimated == False
    assert f3.is_estimated == True # No bill line matched, still waiting
