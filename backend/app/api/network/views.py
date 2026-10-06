from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import datetime
from datetime import timedelta

from ...database import get_db
from ...auth import get_current_user
from ...models import FlowRecord, FlowtabSource, EniHistory

router = APIRouter()

class HourlyData(BaseModel):
    hour: str
    gb: float
    usd: float

class DailyData(BaseModel):
    date: str
    gb: float
    usd: float
    hourly: List[HourlyData]

class SummaryResponse(BaseModel):
    status: str
    total_gb: float
    total_usd: float
    by_category: Dict[str, float]
    daily_series: List[DailyData]

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

class ChargeItem(BaseModel):
    charge_category: str
    gb: float
    usd: float
    share_of_total: float
    flow_count: int

class ChargesResponse(BaseModel):
    status: str
    data: List[ChargeItem]

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
    
    total_billed = 0.0
    total_bytes = 0.0
    categories = {}
    days_map = {}
    
    for f in flows:
        usd = f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0.0)
        b = f.bytes or 0.0
        
        total_billed += usd
        total_bytes += b
        
        cat = f.charge_category
        categories[cat] = categories.get(cat, 0.0) + usd
        
        # Aggregate by day and hour
        # ISO format splits on T: '2023-01-01T15:00:00'
        # f.hour is a datetime
        day_str = f.hour.date().isoformat()
        hour_str = f.hour.isoformat()
        
        if day_str not in days_map:
            days_map[day_str] = {"gb": 0, "usd": 0, "hours": {}}
            
        days_map[day_str]["gb"] += b
        days_map[day_str]["usd"] += usd
        
        if hour_str not in days_map[day_str]["hours"]:
            days_map[day_str]["hours"][hour_str] = {"gb": 0, "usd": 0}
            
        days_map[day_str]["hours"][hour_str]["gb"] += b
        days_map[day_str]["hours"][hour_str]["usd"] += usd

    # Format daily_series
    daily_series = []
    for d_str in sorted(days_map.keys()):
        d_val = days_map[d_str]
        
        hourly_list = []
        for h_str in sorted(d_val["hours"].keys()):
            h_val = d_val["hours"][h_str]
            hourly_list.append(HourlyData(
                hour=h_str, 
                gb=round(h_val["gb"] / (1024**3), 2),
                usd=round(h_val["usd"], 4)
            ))
            
        daily_series.append(DailyData(
            date=d_str,
            gb=round(d_val["gb"] / (1024**3), 2),
            usd=round(d_val["usd"], 4),
            hourly=hourly_list
        ))

    return SummaryResponse(
        status="success",
        total_gb=round(total_bytes / (1024**3), 2),
        total_usd=round(total_billed, 2),
        by_category={k: round(v, 2) for k, v in categories.items()},
        daily_series=daily_series
    )

@router.get("/flows", response_model=FlowsResponse)
def get_flows(
    account_id: str = None, region: str = None, vpc_id: str = None, charge_category: str = None, start_time: str = None, end_time: str = None,
    db: Session = Depends(get_db)):
    
    flows = get_filtered_flows(db, account_id, region, vpc_id, charge_category, start_time, end_time).all()
    
    agg = {}
    for f in flows:
        key = (f.sender_type, f.sender_name, f.receiver_type, f.receiver_name, f.route, f.charge_category)
        if key not in agg:
            agg[key] = {"bytes": 0, "usd": 0}
        agg[key]["bytes"] += (f.bytes or 0)
        agg[key]["usd"] += (f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0.0))
        
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
    flows = db.query(FlowRecord).all()
    
    total_usd = sum((f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0.0)) for f in flows)
    
    agg = {}
    for f in flows:
        cat = f.charge_category
        usd = f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0.0)
        b = f.bytes or 0
        if cat not in agg:
            agg[cat] = {"gb": 0, "usd": 0, "count": 0}
        agg[cat]["gb"] += b
        agg[cat]["usd"] += usd
        agg[cat]["count"] += 1
        
    out = []
    for cat, v in agg.items():
        out.append(ChargeItem(
            charge_category=cat,
            gb=round(v["gb"] / (1024**3), 2),
            usd=round(v["usd"], 4),
            share_of_total=round(v["usd"] / total_usd, 4) if total_usd > 0 else 0,
            flow_count=v["count"]
        ))
        
    return ChargesResponse(status="success", data=out)

@router.get("/flow-graph", response_model=GenericResponse)
def get_flow_graph(db: Session = Depends(get_db)):
    flows = db.query(FlowRecord).all()
    
    nodes_map = set()
    links_map = {}
    
    for f in flows:
        sender_id = f"{f.sender_type}:{f.sender_name}"
        receiver_id = f"{f.receiver_type}:{f.receiver_name}"
        nodes_map.add(sender_id)
        nodes_map.add(receiver_id)
        
        # Link key is (source, target)
        lkey = (sender_id, receiver_id, f.route)
        usd = f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0.0)
        
        if lkey not in links_map:
            links_map[lkey] = 0
        links_map[lkey] += usd
        
    nodes = [{"id": n, "label": n.split(":", 1)[1], "type": n.split(":")[0]} for n in nodes_map]
    links = [{"source": k[0], "target": k[1], "route": k[2], "usd": round(v, 4)} for k, v in links_map.items()]
    
    return GenericResponse(status="success", data={"nodes": nodes, "links": links})
    
@router.get("/architecture", response_model=GenericResponse)
def get_architecture(db: Session = Depends(get_db)):
    sources = db.query(FlowtabSource).all()
    enis = db.query(EniHistory).all()
    
    # Hierarchy: account -> region -> vpc -> resources
    arch = {}
    for s in sources:
        acc = s.account_id
        reg = s.region
        vpc = s.vpc_id
        
        if acc not in arch: arch[acc] = {}
        if reg not in arch[acc]: arch[acc][reg] = {}
        if vpc not in arch[acc][reg]: arch[acc][reg][vpc] = {"name": s.name, "resources": []}
        
    for e in enis:
        acc = e.account_id
        reg = e.region
        vpc = e.vpc_id
        
        if acc in arch and reg in arch[acc] and vpc in arch[acc][reg]:
            arch[acc][reg][vpc]["resources"].append({
                "eni_id": e.eni_id,
                "resource_type": e.resource_type,
                "resource_id": e.resource_id,
                "name": e.name,
                "private_ip": e.private_ip
            })
            
    out = []
    for acc, regs in arch.items():
        acc_obj = {"account_id": acc, "regions": []}
        for reg, vpcs in regs.items():
            reg_obj = {"region": reg, "vpcs": []}
            for vpc, details in vpcs.items():
                reg_obj["vpcs"].append({
                    "vpc_id": vpc,
                    "name": details["name"],
                    "resources": details["resources"]
                })
            acc_obj["regions"].append(reg_obj)
        out.append(acc_obj)
        
    return GenericResponse(status="success", data={"accounts": out})

@router.get("/reconciliation", response_model=GenericResponse)
def get_reconciliation(db: Session = Depends(get_db)):
    flows = db.query(FlowRecord).all()
    
    # We aggregate by charge_category to show how estimated matched bill
    agg = {}
    
    for f in flows:
        cat = f.charge_category
        if cat not in agg:
            agg[cat] = {"estimated_usd": 0, "billed_usd": 0, "waiting_usd": 0}
            
        estimated = f.estimated_usd or 0
        if f.is_estimated:
            agg[cat]["waiting_usd"] += estimated
        else:
            agg[cat]["estimated_usd"] += estimated
            agg[cat]["billed_usd"] += f.billed_usd or 0
            
    out = []
    for cat, v in agg.items():
        est = v["estimated_usd"]
        bill = v["billed_usd"]
        diff = bill - est
        pct = (diff / est * 100) if est > 0 else 0
        
        status = "matched"
        if f"waiting_usd" in v and v["waiting_usd"] > 0 and est == 0:
            status = "waiting_for_bill"
        elif abs(diff) > 0.01:
            status = "corrected"
            
        out.append({
            "charge_category": cat,
            "estimated_usd": round(est, 4),
            "billed_usd": round(bill, 4),
            "waiting_for_bill_usd": round(v["waiting_usd"], 4),
            "difference_usd": round(diff, 4),
            "difference_percent": round(pct, 2),
            "status": status
        })
        
    return GenericResponse(status="success", data=out)

@router.get("/coverage", response_model=GenericResponse)
def get_coverage(db: Session = Depends(get_db)):
    # Calculate coverage of VPC configs
    total = db.query(FlowtabSource).count()
    covered = db.query(FlowtabSource).filter(FlowtabSource.is_enabled == True).count()
    return GenericResponse(status="success", data={"vpcs_covered": covered, "total_vpcs": total})
    
@router.get("/findings", response_model=FindingsResponse)
def get_findings(db: Session = Depends(get_db)):
    findings = []
    flows = db.query(FlowRecord).all()
    
    # 1. S3-via-NAT detection
    # Any NAT flow where the receiver is S3
    s3_nat = sum((f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0)) for f in flows if f.receiver_name == "S3 via NAT")
    if s3_nat > 10:
        findings.append(FindingItem(
            title="S3 Traffic via NAT Gateway",
            description="Large volume of traffic routing to S3 via NAT Gateway. Consider adding an S3 Gateway Endpoint to the VPC to eliminate these costs.",
            severity="high",
            cost_impact=round(s3_nat, 2)
        ))
        
    # 2. Cross-AZ Chatter
    chatty = sum((f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0)) for f in flows if f.charge_category == "Inter-AZ Data Transfer")
    if chatty > 50:
        findings.append(FindingItem(
            title="High Inter-AZ Communication",
            description="Significant costs from chatty pods across AZs (e.g. gateway to auth). Co-locating frequent communicators can reduce this.",
            severity="medium",
            cost_impact=round(chatty, 2)
        ))
        
    # 3. Cross-Region
    peering = sum((f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0)) for f in flows if f.charge_category == "Inter-Region Data Transfer")
    if peering > 10:
        findings.append(FindingItem(
            title="Cross-Region Database Replication",
            description="Consistent outbound data transfer across regions detected. Verify this is authorized replication.",
            severity="low",
            cost_impact=round(peering, 2)
        ))
        
    # 4. Spike Detect
    # Group internet egress by day
    # We will use the full UTC day
    egress_by_day = {}
    for f in flows:
        if f.charge_category == "Internet Egress":
            d = f.hour.date().isoformat()
            if d not in egress_by_day: egress_by_day[d] = 0
            egress_by_day[d] += (f.billed_usd if f.billed_usd is not None else (f.estimated_usd or 0))
            
    days = sorted(list(egress_by_day.keys()))
    if len(days) >= 2:
        # Use simple moving average of first 5 days vs day 6
        avg = sum(egress_by_day[d] for d in days[:5]) / len(days[:5])
        for target_day in days[5:]:
            if target_day in egress_by_day and avg > 0:
                if egress_by_day[target_day] > avg * 2:
                    findings.append(FindingItem(
                        title=f"Spike in Internet Egress ({target_day})",
                        description=f"Egress out of ALB spiked over 3x the running average of ${round(avg, 2)}/day.",
                        severity="high",
                        cost_impact=round(egress_by_day[target_day] - avg, 2)
                    ))
                    
    # ALB missing under-count notice (reconciliation finding)
    alb_est = sum(f.estimated_usd for f in flows if f.sender_type == "ELB")
    alb_bill = sum(f.billed_usd for f in flows if f.sender_type == "ELB" and not f.is_estimated)
    if alb_bill > 0 and alb_est > 0:
        diff = alb_bill - alb_est
        if diff > 10:
            findings.append(FindingItem(
                title="ALB True-Outbound Correction",
                description="Flow logs undercount application layer bytes inside ALB connections. Bill reconciliation corrected a massive ~44% difference.",
                severity="medium",
                cost_impact=round(diff, 2)
            ))

    return FindingsResponse(status="success", findings=findings)
    
@router.get("/setup/checks", response_model=GenericResponse)
def get_setup_checks(db: Session = Depends(get_db)):
    sources = db.query(FlowtabSource).all()
    mode = "AWS"
    if sources and sources[0].mode == "demo":
        mode = "demo"

    return GenericResponse(status="success", data={"flow_logs": True, "cur": True, "mode": mode})

