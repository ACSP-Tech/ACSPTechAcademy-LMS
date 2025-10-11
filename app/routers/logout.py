from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.register import MessageOut
from ..crud.logout import logout_user
from ..database_setup import get_db
from ..dep.authen import user_auth

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/logout", status_code=status.HTTP_201_CREATED, response_model=MessageOut)
async def user_logout(token=Depends(user_auth), session=Depends(get_db)):
    """
    logout route, frontend integration: blacklist user token on logout
    Args: 
        token: authenticated user token, default to user_auth dependency header bearer token from login
        session: database session, default to system get_db
        raises:
            HTTPException 500 for internal server error and 404, 403, 401 for unauthorized access
    Returns:
        MessageOut output schema, 201 created
        send verification email to client
    """
    try:
        return await logout_user(token, session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )