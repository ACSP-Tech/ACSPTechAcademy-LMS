from ..schema.login import LogOut
from ..model.lms_tables import Users
from ..utils.payload import encode_token
from sqlmodel import select
from fastapi import HTTPException, status
from ..utils.hash_password import password_verify
from ..utils.background_email import send_verification_email


async def user_login(data, session, backgroundtask):
    try:
        statement = select(Users).where(Users.email == data.email)
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= f"User with mail {data.email} not found"
            )
        verify = await password_verify(data.password, user.hashed_password)
        if not verify:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password")
        if not user.verify:
            payload = {
                "email": user.email,
                "first_name": user.first_name,
                "phone_number": user.phone_number,
                "type": "email_verification"
            }
            email_token = await encode_token(payload)
            backgroundtask.add_task(
                send_verification_email,
                email=user.email,
                token=email_token,
                username=user.first_name
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"account not verified, verification mail has been resent, please verify your account before login"
            )
        payload = {
            "email": user.email,
            "id": user.id,
            "role": user.role
        }
        user_token = await encode_token(payload)
        return LogOut(
            role=user.role,
            first_name=user.first_name,
            token=user_token,
            token_type="bearer"
        )
    except HTTPException as Httpexc:
        raise Httpexc

        
        
        