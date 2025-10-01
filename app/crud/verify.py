from ..utils.payload import decode_token
from ..model.lms_tables import Users
from sqlmodel import select, and_
from fastapi import HTTPException, status
from ..utils.background_email import send_welcome_email
from ..schema.register import MessageOut

async def verify_user(token, backgroundtask, session):
    try:
        payload = await decode_token(token)
        user_type = payload.get("type")
        phone_number = payload.get("phone_number")
        email = payload.get("email")
        if user_type != "email_verification":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token type"
            )
        statement = select(Users).where(and_(Users.email == email, Users.phone_number == phone_number))
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="user account not found"
            )
        if user.verify:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified"
            )
        user.verify = True
        backgroundtask.add_task(
            send_welcome_email,
            email=user.email,
            username=user.first_name
        )
        response = "Email verified successfully! Check your mail for the next steps, You can now login."
        return MessageOut(
            message=response
        )
    except HTTPException as Httpexc:
        await session.rollback()
        raise Httpexc
