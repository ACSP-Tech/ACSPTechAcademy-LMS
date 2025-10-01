from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from ..schema.register import Register, RegisterOut
from ..crud.register import user_register
from ..database_setup import get_db

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def register(data:Register, backgroundtask:BackgroundTasks, session=Depends(get_db), response_model=RegisterOut):
    """
    registration route
    Args: 
        data: Register Input Schema, Body parameter
        background_tasks: default FastAPI background tasks for sending email
        session: database session, default to system get_db
        raises:
            HTTPException 500 for internal server error and 400 conflict for duplicate email
    Returns:
        RegisterOut output schema
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