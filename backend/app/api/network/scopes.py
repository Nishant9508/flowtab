from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database import get_db
from ...models import FlowtabSource

router = APIRouter()

@router.get("/")
def list_scopes(db: Session = Depends(get_db)):
    """List all accounts and VPCs discovered/configured in the environment."""
    sources = db.query(FlowtabSource).all()
    
    # Group by account and region
    accounts = {}
    for src in sources:
        acc = src.account_id
        if acc not in accounts:
            accounts[acc] = {'regions': set(), 'vpcs': []}
        accounts[acc]['regions'].add(src.region)
        accounts[acc]['vpcs'].append({
            "vpc_id": src.vpc_id,
            "region": src.region,
            "name": src.name,
            "mode": src.mode,
            "is_enabled": src.is_enabled
        })
        
    return {
        "status": "success",
        "accounts": [
            {
                "account_id": a, 
                "regions": list(v['regions']), 
                "vpcs": v['vpcs']
            } for a, v in accounts.items()
        ]
    }
