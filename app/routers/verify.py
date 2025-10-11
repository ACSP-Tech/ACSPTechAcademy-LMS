from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from ..database_setup import get_db
from ..schema.register import MessageOut
from ..crud.verify import verify_user

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.get("/verify-email", status_code=status.HTTP_202_ACCEPTED, response_model=MessageOut)
async def email_verification(token: str, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 2: user verification flow
    Verification route by users, verification can only occur once.
    Args:
        token: query paramenter from user verification url sent
        session : Default to database session
        raises:
        400 Bad request for email already verified, 500 for internal server error
    Returns:
        MessageOut output schema, 202 created
        send welcome email to client with whatsapp channel onboarding and next steps
    """
    try:
        return await verify_user(token, backgroundtask, session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
