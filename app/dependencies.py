from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.auth_service import decode_jwt_token  # adjust if needed

# DATABASE DEPENDENCY
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ROLE-BASED ACCESS CONTROL
def require_roles(*roles):
    def role_checker(current_user = Depends(decode_jwt_token)):
        user_roles = current_user.get("roles", [])
        if not any(r in user_roles for r in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {roles}, you have: {user_roles}"
            )
        return current_user
    return role_checker
