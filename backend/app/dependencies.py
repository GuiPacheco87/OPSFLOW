from fastapi import Depends,HTTPException
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import Role,User
from .security import decode_token
bearer=HTTPBearer()
def current_user(credentials:HTTPAuthorizationCredentials=Depends(bearer),db:Session=Depends(get_db))->User:
    try: payload=decode_token(credentials.credentials)
    except Exception: raise HTTPException(401,"Token inválido ou expirado")
    user=db.get(User,payload["sub"])
    if not user or not user.active or user.organization_id!=payload.get("org"): raise HTTPException(401,"Usuário inválido")
    return user
def require(*roles:Role):
    def check(user:User=Depends(current_user)):
        if user.role not in roles: raise HTTPException(403,"Permissão insuficiente")
        return user
    return check
