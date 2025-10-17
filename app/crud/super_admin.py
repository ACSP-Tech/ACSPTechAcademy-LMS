from ..utils.payload import decode_token
from ..model.lms_tables import Users, BlackList
from fastapi import HTTPException, status
from sqlmodel import select, and_
from sqlalchemy.orm import defer
from fastapi_pagination.ext.sqlalchemy import paginate

async def get_all_users(params, session, token):
    try:
        statement = select(Users).options(defer(Users.hashed_password), 
                                                defer(Users.profile_public_id)).where(Users.role != "superadmin").order_by(Users.created_at.desc())
        return await paginate(session, statement, params)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    