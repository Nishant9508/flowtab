from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from ..models import BilledLine, FlowRecord

def allocate_bill_to_flows(db: Session, hour, vpc_id: str):
    """
    Takes exactly billed lines from the CUR and allocates their USD proportionally
    to the estimated flows.
    """
    # Grab all flows for this hour/vpc that are currently marked estimated
    flows = db.query(FlowRecord).filter(
        FlowRecord.hour == hour,
        FlowRecord.vpc_id == vpc_id,
        FlowRecord.is_estimated == True
    ).all()
    
    if not flows:
        return
        
    # Grab billed lines for this hour
    # We would normally filter by account/region of the VPC. Assumed here.
    billed_lines = db.query(BilledLine).filter(
        BilledLine.hour == hour
    ).all()
    
    # Normally, if a BilledLine has a resource_id (e.g. NAT Gateway ID), we allocate ONLY
    # to flows where sender_id == resource_id or receiver_id == resource_id.
    # For this simplified version, let's group by charge category (e.g. "Internet Egress")
    
    billed_by_category = {}
    for line in billed_lines:
        cat = line.usage_type # Assuming setup maps usage_type to category
        billed_by_category[cat] = billed_by_category.get(cat, 0.0) + line.cost_usd
        
    # Group flows by category
    flows_by_category = {}
    for f in flows:
        cat = f.charge_category
        if cat not in flows_by_category:
            flows_by_category[cat] = []
        flows_by_category[cat].append(f)
        
    # Allocate proportionally
    for cat, items in flows_by_category.items():
        total_estimated = sum(f.estimated_usd for f in items)
        
        # If we have a bill for this category
        if cat in billed_by_category and billed_by_category[cat] > 0:
            total_billed = billed_by_category[cat]
            for f in items:
                # Proportional allocation, or fallback to equal split if estimate was 0
                if total_estimated > 0:
                    fraction = f.estimated_usd / total_estimated
                else:
                    fraction = 1.0 / len(items)
                    
                f.billed_usd = total_billed * fraction
                f.is_estimated = False
        else:
            # If no bill yet (waiting for CUR), or no charge, billed_usd just falls back to estimated
            for f in items:
                f.billed_usd = f.estimated_usd
                # Stays is_estimated = True so we can run this again when the bill arrives
                
    db.commit()
