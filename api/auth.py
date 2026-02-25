from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.models import User, UserRole
from core.database import get_db
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # In prod: Decode JWT here
    user = db.query(User).filter(User.email == token).first() # Simulating token=email for simplicity
    if not user:
        raise HTTPException(status_code=401, detail="Invalid auth")
    return user

def require_architect(user: User = Depends(get_current_user)):
    if user.role not in [UserRole.ADMIN, UserRole.ARCHITECT]:
        raise HTTPException(status_code=403, detail="Need Architect role")
    return user