from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ...network.alerts import generate_insights
from ...models import FlowtabSource

router = APIRouter()

@router.get("/")
def get_insights(db: Session = Depends(get_db)):
    """Returns insights across all active VPCs"""
    sources = db.query(FlowtabSource).all()
    all_insights = []
    
    for src in sources:
        insights = generate_insights(db, src.vpc_id)
        for i in insights:
            if i["title"] != "Network Optimized":
                i["vpc"] = src.name
                all_insights.append(i)
                
    if not all_insights:
        return {"status": "success", "insights": [{"title": "Network Optimized", "description": "No major anti-patterns detected.", "severity": "low", "cost_impact": 0.0, "vpc": "All"}]}
        
    all_insights.sort(key=lambda x: x["cost_impact"], reverse=True)
    return {"status": "success", "insights": all_insights}
