from sqlalchemy.orm import Session
from ..models import FlowRecord

def generate_insights(db: Session, vpc_id: str):
    """
    Analyzes flows for known antipatterns and returns plain-language insights.
    """
    flows = db.query(FlowRecord).filter(FlowRecord.vpc_id == vpc_id).all()
    insights = []
    
    # Check for heavy Cross-AZ chatter
    cross_az_flows = [f for f in flows if f.route == "cross-az"]
    cross_az_cost = sum(f.billed_usd for f in cross_az_flows if f.billed_usd)
    if cross_az_cost > 0.05:
        # Get top sender
        top_sender = max(cross_az_flows, key=lambda f: f.billed_usd).sender_name
        insights.append({
            "title": "High Cross-AZ Chatter",
            "description": f"You spent ${cross_az_cost:.2f} on Inter-AZ data transfer. The primary driver is '{top_sender}'. Consider co-locating workloads in the same Availability Zone or using a local cache.",
            "severity": "medium",
            "cost_impact": cross_az_cost
        })
        
    # Check for NAT gateway inefficiencies (e.g., S3 traffic going through NAT)
    nat_flows = [f for f in flows if f.route == "nat-egress"]
    s3_through_nat_cost = sum(f.billed_usd for f in nat_flows if "S3" in (f.receiver_name or "") and f.billed_usd)
    if s3_through_nat_cost > 1.0:
        insights.append({
            "title": "Missing S3 VPC Endpoint",
            "description": f"You are paying ${s3_through_nat_cost:.2f} to route S3 traffic through a NAT Gateway. Create a Gateway VPC Endpoint for S3 (which is free) to eliminate this cost immediately.",
            "severity": "high",
            "cost_impact": s3_through_nat_cost
        })
        
    # Default insight if well optimized
    if not insights:
        insights.append({
            "title": "Network Optimized",
            "description": "No major anti-patterns detected in the current flow logs.",
            "severity": "low",
            "cost_impact": 0.0
        })
        
    insights.sort(key=lambda x: x["cost_impact"], reverse=True)
    return insights
