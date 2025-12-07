# app/services/auth_service.py
from fastapi import Depends, Header, HTTPException, status
from typing import Optional, Dict

# Try to use PyJWT if available. If not, we'll fallback to a simple dev stub.
try:
    import jwt  # PyJWT
    _HAS_PYJWT = True
except Exception:
    _HAS_PYJWT = False

# Secret & algorithm — in prod load from env/config
_JWT_SECRET = "CHANGE_THIS_SECRET_FOR_PRODUCTION"
_JWT_ALGO = "HS256"

def _decode_with_pyjwt(token: str) -> Dict:
    try:
        payload = jwt.decode(token, _JWT_SECRET, algorithms=[_JWT_ALGO])
        # expected payload to contain: {"sub": user_id, "roles": ["admin", ...], ...}
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def _dev_token_stub(token: str) -> Dict:
    # Developer fallback: accept token "devtoken" and return a sample user payload.
    # You can change returned roles/user id as needed during local development.
    if token == "devtoken" or token == "DEV" or token == "Bearer devtoken":
        return {"sub": 1, "id": 1, "username": "dev", "roles": ["admin", "manager"]}
    # Also allow empty token if you need: (not recommended)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

async def decode_jwt_token(authorization: Optional[str] = Header(None)) -> Dict:
    """
    FastAPI dependency that returns the decoded token (dict).
    Use in dependencies.py as: Depends(decode_jwt_token)
    Expected Authorization header: "Bearer <token>"
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")

    # Handle various header forms
    auth = authorization.strip()
    if auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1].strip()
    else:
        # If header is just token, accept it too
        token = auth

    if _HAS_PYJWT:
        return _decode_with_pyjwt(token)
    else:
        # Fallback dev mode
        return _dev_token_stub(token)
