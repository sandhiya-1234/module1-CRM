from fastapi import Depends, HTTPException, status

# Temporary dummy user (replace with Pod A integration later)
def get_current_user():
    # Simulate a logged-in user
    return {"id": 1, "roles": ["admin"]}  # ❌ Change role to test 403

def require_roles(*allowed_roles):
    def decorator(current_user: dict = Depends(get_current_user)):
        user_roles = current_user.get("roles", [])
        print("DEBUG >> Current user roles:", user_roles)  # ✅ helps debug in terminal

        # Check if any role matches the allowed roles
        if not any(role in allowed_roles for role in user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {allowed_roles}, you have: {user_roles}"
            )
        return current_user  # ✅ return so routes can still access it
    return decorator

# app/api/security.py
from fastapi import APIRouter, Depends
from app.api.security import require_roles, get_current_user  # if both in same file, adjust import

router = APIRouter(prefix="/secure", tags=["security"])

@router.get("/finance")
def secure_finance_demo(current_user=Depends(require_roles("admin", "manager"))):
    """
    🔒 Secure Finance Demo
    Accessible only by admin or manager roles.
    """
    return {
        "message": f"Welcome {current_user['id']}, you have access to secure finance data!",
        "roles": current_user.get("roles", [])
    }
