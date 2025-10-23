from fastapi.security import OAuth2PasswordBearer
from app.database_setup import get_db
from fastapi import Depends, HTTPException, status
from ..utils.authen import is_blacklisted
from ..utils.payload import decode_token

# Define OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

async def user_auth(token=Depends(oauth2_scheme), session=Depends(get_db)):
   """
   user authentication dependency.
   """
   try:
       await is_blacklisted(token, session)
       return token 
   except Exception as e:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail=str(e)
       )
   
async def student_auth(token=Depends(user_auth)):
    """
    Dependency to ensure the user is an admin or superadmin.
    """
    try:
        payload = await decode_token(token)
        role = payload.get("role")
        if role not in ["student", "teacher", "admin", "superadmin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="At least student privileges required."
            )
        return token
    except HTTPException as http_exc:
       raise http_exc 
   
async def teacher_auth(token=Depends(user_auth)):
    """
    Dependency to ensure the user is an admin or superadmin.
    """
    try:
        payload = await decode_token(token)
        role = payload.get("role")
        if role not in ["teacher", "admin", "superadmin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="At least teacher privileges required."
            )
        return token
    except HTTPException as http_exc:
       raise http_exc   
   
async def admin_auth(token=Depends(user_auth)):
    """
    Dependency to ensure the user is an admin or superadmin.
    """
    try:
        payload = await decode_token(token)
        role = payload.get("role")
        if role not in ["admin", "superadmin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="At least admin privileges required."
            )
        return token
    except HTTPException as http_exc:
       raise http_exc
   
async def superadmin_auth(token=Depends(user_auth)):
   """
   Dependency to ensure the user is a superadmin.
   """
   try:
       payload = await decode_token(token)
       role = payload.get("role")
       if role != "superadmin":
           raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail="Superadmin privileges required."
           )
       return token
   except HTTPException as http_exc:
       raise http_exc