from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from ..schema.login import LoginUser, LogOut
from ..database_setup import get_db
from ..crud.login import user_login

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/signin", response_model=LogOut, status_code=status.HTTP_200_OK)
async def Login(data:LoginUser, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    User Login API
    Args:
        data: LoginUser Schema Body parameter
        session: default to database session
        raise:
    Returns:
        Logout schema json response
        200 ok response
    """
    try:
        return await user_login(data, session, backgroundtask)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )