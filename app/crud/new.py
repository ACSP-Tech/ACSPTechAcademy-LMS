from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from ..schema.register import Register, RegisterOut
from ..crud.register import user_register
from ..database_setup import get_db
from ..utils.email import send_verification_email
from ..utils.token import create_verification_token

router = APIRouter(prefix="/user", tags=["User Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=RegisterOut)
async def register(
    data: Register, 
    background_tasks: BackgroundTasks,
    session=Depends(get_db)
):
    """
    Registration route with email verification
    
    Args: 
        data: Register Input Schema, Body parameter
        background_tasks: FastAPI background tasks for sending email
        session: database session, default to system get_db
        
    Raises:
        HTTPException 500 for internal server error and 400 conflict for duplicate email
        
    Returns:
        RegisterOut output schema with message about verification email
    """
    try:
        # Create user (but keep them unverified)
        user = await user_register(data, session)
        
        # Generate verification token (JWT with user email)
        verification_token = create_verification_token(user.email)
        
        # Send verification email in background
        background_tasks.add_task(
            send_verification_email,
            email=user.email,
            token=verification_token,
            username=user.username  # or user.first_name
        )
        
        return user
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.get("/verify-email")
async def verify_email(token: str, session=Depends(get_db)):
    """
    Email verification endpoint - user clicks link in email
    
    Args:
        token: Verification token from email link
        session: database session
        
    Returns:
        Success message
    """
    try:
        from ..utils.token import verify_verification_token
        from ..crud.register import activate_user
        
        # Decode and verify token
        email = verify_verification_token(token)
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token"
            )
        
        # Activate user in database
        activated = await activate_user(email, session)
        
        if not activated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {
            "message": "Email verified successfully! You can now login.",
            "verified": True
        }
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(e)}"
        )


@router.post("/resend-verification")
async def resend_verification(
    email: str,
    background_tasks: BackgroundTasks,
    session=Depends(get_db)
):
    """
    Resend verification email if user didn't receive it
    
    Args:
        email: User's email address
        background_tasks: FastAPI background tasks
        session: database session
        
    Returns:
        Success message
    """
    try:
        from ..crud.register import get_user_by_email
        
        # Check if user exists
        user = await get_user_by_email(email, session)
        
        if not user:
            # Don't reveal if email exists or not (security)
            return {"message": "If that email exists, a verification link has been sent"}
        
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        
        # Generate new token
        verification_token = create_verification_token(user.email)
        
        # Send email
        background_tasks.add_task(
            send_verification_email,
            email=user.email,
            token=verification_token,
            username=user.username
        )
        
        return {"message": "Verification email sent"}
        
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )