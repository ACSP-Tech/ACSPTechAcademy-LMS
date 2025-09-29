from ..model.lms_tables import BlackList, Users
from sqlmodel import select
from fastapi import HTTPException, status
from sqlalchemy import and_
from .payload import decode_token



async def is_blacklisted(token, session) -> bool:
    try:
        payload = decode_token(token)
        email = payload.get("email")
        id = payload.get("id")
        statement = select(Users).where(and_(Users.email == email, Users.id == id))
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if not user.verify:
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Check your mail and Verify your account first") 
        if not user.is_active:
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account has been blocked due to flagged activities, please contact admin")
        statement = select(BlackList).where(BlackList.black_token == token)
        stat_result = await session.execute(statement)
        result = stat_result.scalars().first()
        if result:
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has been blacklisted. Please log in again.")
        return False
    except HTTPException as http_exc:
        raise http_exc