from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Mock JWT token verification. 
    In production, this validates against an OIDC provider (e.g., Auth0, Azure AD)
    or verifies a local admin token.
    """
    if os.getenv("DEMO_MODE", "true").lower() == "true":
        return {"sub": "demo-user", "role": "admin"}
        
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    token = credentials.credentials
    if token != "secret-local-admin-token": # Only for illustration
        raise HTTPException(status_code=401, detail="Invalid token")
        
    return {"sub": "admin", "role": "admin"}

def get_current_user(user: dict = Depends(verify_token)):
    return user
