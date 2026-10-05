from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from tests.generator.demo_data import generate_demo_scenario

router = APIRouter()

class GenerateDemoRequest(BaseModel):
    account_id: str = "demo-123456"
    region: str = "us-east-1"
    
@router.post("/generate")
def generate_demo_data(request: GenerateDemoRequest, db: Session = Depends(get_db)):
    generate_demo_scenario(db, account_id=request.account_id, region=request.region, vpc_id="vpc-demo-main")
    return {"status": "success", "message": "Demo data generated"}
