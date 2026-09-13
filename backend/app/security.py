from datetime import datetime,timedelta,timezone
import jwt
from pwdlib import PasswordHash
from .config import settings
hashing=PasswordHash.recommended()
def hash_password(value:str)->str: return hashing.hash(value)
def verify_password(value:str,hashed:str)->bool: return hashing.verify(value,hashed)
def create_token(user_id:str,organization_id:str)->str: return jwt.encode({"sub":user_id,"org":organization_id,"exp":datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)},settings.jwt_secret,algorithm="HS256")
def decode_token(token:str)->dict: return jwt.decode(token,settings.jwt_secret,algorithms=["HS256"])

