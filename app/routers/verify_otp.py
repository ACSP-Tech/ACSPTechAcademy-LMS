from fastapi import APIRouter, Depends, status, HTTPException
from ..schema.register import MessageOut
from ..schema.forgot_password import verifyOTP
from ..database_setup import get_db
from ..crud.verify_otp import user_verify_otp

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/verify-otp", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def otp_verification(data:verifyOTP, session=Depends(get_db)):
    """
    step 2: verify OTP endpoint, frontend integration
    Args: 
        data: verify otp Input Schema, Body parameter
        background_tasks: default FastAPI background tasks for sending email
        session: database session, default to system get_db
        raises:
            HTTPException 500 for internal server error and 400 bad request for incorrect or expired OTP, incorrect email
    Returns:
        MessageOut output schema, 200 OK
        send password reset email to client
    """
    try:
        return await user_verify_otp(data, session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )