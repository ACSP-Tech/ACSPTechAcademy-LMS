from fastapi import APIRouter, Depends, status, HTTPException
from ..schema.register import MessageOut
from ..schema.forgot_password import Reset
from ..database_setup import get_db
from ..crud.reset_password import user_reset_password

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/reset-password", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def password_reset(data:Reset, session=Depends(get_db)):
    """
    step 3: reset password endpoint, frontend integration
    Args: 
        data: Reset Input Schema, Body parameter
        session: database session, default to system get_db
        raises:
            HTTPException 500 for internal server error and 400 conflict for duplicate email or phone_number
    Returns:
        MessageOut output schema, 200 OK
        send password reset email to client
    """
    try:
        return await user_reset_password(data, session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )