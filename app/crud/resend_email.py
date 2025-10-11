from sqlmodel import select, and_
from fastapi import HTTPException, status
from ..utils.payload import encode_email_token
from ..utils.background_email import send_verification_email
from ..schema.register import MessageOut
from ..model.lms_tables import Users

async def resend_email_verification(data, session, backgroundtask):
    try:
        #check if user exist
        statement = select(Users).where(Users.email == data.email)
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            response = f"Verification email resent, Kindly check {data.email} inbox or spam folder to verify your account"
            return MessageOut(message=response)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user, contact support"
            )
        if user.verify:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your account is already verified"
            )
        payload = {
            "email": user.email,
            "first_name": user.first_name,
            "phone_number": user.phone_number,
            "type": "email_verification"
        }
        email_token = await encode_email_token(payload)
        backgroundtask.add_task(
            send_verification_email,
            email=data.email,
            token=email_token,
            username=user.first_name
        )
        response = f"Verification email resent, Kindly check {data.email} inbox or spam folder to verify your account"
        return MessageOut(message=response)
    except HTTPException as Httpexc:
        session.rollback()
        raise Httpexc