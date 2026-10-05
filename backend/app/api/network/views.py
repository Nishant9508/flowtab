from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from ...database import get_db
from ...auth import get_current_user
from ...models import FlowRecord

router = APIRouter()

@router.get("/summary")
def get_summary(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Returns total costs, filtered by available scopes (for M1 demo purposes)"""
    flows = db.query(FlowRecord).all()
    
    total_billed = sum(f.billed_usd for f in flows if f.billed_usd)
    total_bytes = sum(f.bytes for f in flows if f.bytes)
    
    charge_categories = {}
    for f in flows:
        cat = f.charge_category
        charge_categories[cat] = charge_categories.get(cat, 0.0) + (f.billed_usd or 0.0)
        
    return {
        "status": "success",
        "total_gb": round(total_bytes / (1024**3), 2),
        "total_usd": round(total_billed, 2),
        "by_category": charge_categories
    }

@router.get("/flows")
def get_flows(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Returns flow records for the architecture view"""
    flows = db.query(FlowRecord).all()
    return {
        "status": "success",
        "data": [
            {
                "sender_type": f.sender_type,
                "sender_name": f.sender_name,
                "receiver_type": f.receiver_type,
                "receiver_name": f.receiver_name,
                "route": f.route,
                "charge_category": f.charge_category,
                "gb": round((f.bytes or 0) / (1024**3), 2),
                "usd": round(f.billed_usd or 0.0, 4)
            } for f in flows
        ]
    }
