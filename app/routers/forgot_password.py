from fastapi import APIRouter, Depends, BackgroundTasks, status, HTTPException
from ..schema.register import MessageOut
from ..schema.forgot_password import ForgotPassword
from ..database_setup import get_db
from ..crud.forgot_password import user_forgot_password

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/forgot-password", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def forgot_password(data:ForgotPassword, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 1: initiate
    forgot password endpoint, frontend integration
    Args: 
        data: Forgot Password Input Schema, Body parameter
        session: database session, default to system get_db
        raises:
            HTTPException 500 for internal server error
    Returns:
        MessageOut output schema, 200 OK
        send password reset email to client
    """
    try:
        return await user_forgot_password(data, session, backgroundtask)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )