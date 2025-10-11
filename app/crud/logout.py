from ..utils.payload import decode_token
from ..model.lms_tables import BlackList
from fastapi import HTTPException, status
from sqlmodel import select
from ..schema.register import MessageOut


async def logout_user(token, session):
    try:
        payload = await decode_token(token)
        id = payload.get("id")
        new_blacklist = BlackList(black_token=token, user_id=id)
        session.add(new_blacklist)
        await session.commit()
        await session.refresh(new_blacklist)
        response = "Logout Successfully"
        return MessageOut(message=response)
    except HTTPException as http_exc:
        await session.rollback()
        raise http_exc