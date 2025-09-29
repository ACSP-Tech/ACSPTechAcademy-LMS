from app.sec import SECRET_KEY, ALGORITHM
import jwt
from fastapi import HTTPException, status

def decode_token(token):
   try:
       payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
       return payload
  
   except jwt.ExpiredSignatureError:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Token has expired. Please log in again.",
       )
   except jwt.InvalidTokenError:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Invalid token. Please log in again.",
       )