from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from ..schema.register import Register, MessageOut
from ..crud.register import user_register
from ..database_setup import get_db

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=MessageOut)
async def register(data:Register, backgroundtask:BackgroundTasks, session=Depends(get_db)):
    """
    step 1: user verification flow
    registration route, frontend integration: create user, send verification email to user
    Args: 
        data: Register Input Schema, Body parameter
        background_tasks: default FastAPI background tasks for sending email
        session: database session, default to system get_db
        raises:
            HTTPException 500 for internal server error and 409 conflict for duplicate email or phone_number
    Returns:
        MessageOut output schema, 201 created
        send verification email to client
    """
    try:
        return await user_register(data, session, backgroundtask)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )