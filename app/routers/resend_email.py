from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from ..schema.register import MessageOut
from ..crud.resend_email import resend_email_verification
from ..database_setup import get_db
from ..schema.resend_email import Resend

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/resend-email", status_code=status.HTTP_201_CREATED, response_model=MessageOut)
async def resend_email(data:Resend, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 3: user verification flow(should in case user did not receive verification email, or token expired)
    resend email verification endpoint, frontend integration
    Args: 
        data: resend Input Schema, Body parameter
        background_tasks: default FastAPI background tasks for sending email
        session: database session, default to system get_db
        raises:
            HTTPException 500 for internal server error and 400 bad request for already verified email
    Returns:
        MessageOut output schema, 201 created
        send verification email to client
    """
    try:
        return await resend_email_verification(data, session, backgroundtask)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )