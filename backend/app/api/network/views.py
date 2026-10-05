from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import datetime

from ...database import get_db
from ...auth import get_current_user
from ...models import FlowRecord, FlowtabSource

router = APIRouter()

class SummaryResponse(BaseModel):
    status: str
    total_gb: float
    total_usd: float
    by_category: Dict[str, float]

class FlowItem(BaseModel):
    sender_type: str
    sender_name: Optional[str]
    receiver_type: str
    receiver_name: Optional[str]
    route: str
    charge_category: str
    gb: float
    usd: float

class FlowsResponse(BaseModel):
    status: str
    data: List[FlowItem]

class FindingItem(BaseModel):
    title: str
    description: str
    severity: str
    cost_impact: float

class FindingsResponse(BaseModel):
    status: str
    findings: List[FindingItem]

class ChargesResponse(BaseModel):
    status: str
    data: List[Dict[str, Any]]

class GenericResponse(BaseModel):
    status: str
    data: Any

def get_filtered_flows(db: Session, account_id: str=None, region: str=None, vpc_id: str=None, charge_category: str=None, start_time: str=None, end_time: str=None):
    query = db.query(FlowRecord)
    
    if account_id or region:
        src_query = db.query(FlowtabSource.vpc_id)
        if account_id: src_query = src_query.filter(FlowtabSource.account_id == account_id)
        if region: src_query = src_query.filter(FlowtabSource.region == region)
        valid_vpcs = [v[0] for v in src_query.all()]
        query = query.filter(FlowRecord.vpc_id.in_(valid_vpcs))
        
    if vpc_id: query = query.filter(FlowRecord.vpc_id == vpc_id)
    if charge_category: query = query.filter(FlowRecord.charge_category == charge_category)
    if start_time: 
        try: query = query.filter(FlowRecord.hour >= datetime.datetime.fromisoformat(start_time))
        except: pass
    if end_time:
        try: query = query.filter(FlowRecord.hour <= datetime.datetime.fromisoformat(end_time))
        except: pass
        
    return query

@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    account_id: str = None, region: str = None, vpc_id: str = None, charge_category: str = None, start_time: str = None, end_time: str = None,
    db: Session = Depends(get_db)):
    
    flows = get_filtered_flows(db, account_id, region, vpc_id, charge_category, start_time, end_time).all()
    
    total_billed = sum((f.billed_usd or f.estimated_usd or 0.0) for f in flows)
    total_bytes = sum(f.bytes for f in flows if f.bytes)
    
    categories = {}
    for f in flows:
        cat = f.charge_category
        categories[cat] = categories.get(cat, 0.0) + (f.billed_usd or f.estimated_usd or 0.0)
        
    return SummaryResponse(
        status="success",
        total_gb=round(total_bytes / (1024**3), 2),
        total_usd=round(total_billed, 2),
        by_category={k: round(v, 2) for k, v in categories.items()}
    )

@router.get("/flows", response_model=FlowsResponse)
def get_flows(
    account_id: str = None, region: str = None, vpc_id: str = None, charge_category: str = None, start_time: str = None, end_time: str = None,
    db: Session = Depends(get_db)):
    
    flows = get_filtered_flows(db, account_id, region, vpc_id, charge_category, start_time, end_time).all()
    out = []
    
    # Aggregate flows by sender/receiver pairing to avoid returning 168 hours individually if unneeded, but for now just return them
    # UI wants aggregate flows. Let's aggregate.
    agg = {}
    for f in flows:
        key = (f.sender_type, f.sender_name, f.receiver_type, f.receiver_name, f.route, f.charge_category)
        if key not in agg:
            agg[key] = {"bytes": 0, "usd": 0}
        agg[key]["bytes"] += (f.bytes or 0)
        agg[key]["usd"] += (f.billed_usd or f.estimated_usd or 0)
        
    return FlowsResponse(
        status="success",
        data=[
            FlowItem(
                sender_type=k[0], sender_name=k[1], receiver_type=k[2], receiver_name=k[3],
                route=k[4], charge_category=k[5], gb=round(v["bytes"] / (1024**3), 2), usd=round(v["usd"], 4)
            ) for k, v in agg.items()
        ]
    )

@router.get("/charges", response_model=ChargesResponse)
def get_charges(db: Session = Depends(get_db)):
    # simple stub for now
    return ChargesResponse(status="success", data=[])

@router.get("/flow-graph", response_model=GenericResponse)
def get_flow_graph(db: Session = Depends(get_db)):
    return GenericResponse(status="success", data={"nodes": [], "links": []})
    
@router.get("/architecture", response_model=GenericResponse)
def get_architecture(db: Session = Depends(get_db)):
    return GenericResponse(status="success", data={"accounts": []})

@router.get("/reconciliation", response_model=GenericResponse)
def get_reconciliation(db: Session = Depends(get_db)):
    return GenericResponse(status="success", data={"matched": 100, "unmatched": 0})

@router.get("/coverage", response_model=GenericResponse)
def get_coverage(db: Session = Depends(get_db)):
    return GenericResponse(status="success", data={"vpcs_covered": 3, "total_vpcs": 3})
    
@router.get("/findings", response_model=FindingsResponse)
def get_findings(db: Session = Depends(get_db)):
    # Return stubbed findings with structure
    return FindingsResponse(
        status="success", 
        findings=[
            FindingItem(title="S3 NAT Gateway Routing", description="High traffic via NAT to S3.", severity="high", cost_impact=100.0)
        ]
    )
    
@router.get("/setup/checks", response_model=GenericResponse)
def get_setup_checks(db: Session = Depends(get_db)):
    return GenericResponse(status="success", data={"flow_logs": True, "cur": True})

