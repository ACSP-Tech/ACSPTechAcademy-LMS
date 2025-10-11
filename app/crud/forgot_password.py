from sqlmodel import select, and_, update
from fastapi import HTTPException, status
from ..model.lms_tables import Users, OTP
from datetime import datetime, timedelta, timezone
from ..schema.register import MessageOut
from ..utils.otp import generate_otp
from ..utils.background_email import send_otp_email

OTP_EXPIRY_MINUTES = 5


async def user_forgot_password(data, session, backgroundtask):
    try:
        user_email = data.email
        #check if user exist
        statement = select(Users).where(Users.email == user_email)
        result = await session.execute(statement)
        user = result.scalars().first()
        if not user:
            response = f"An OTP has been sent to {data.email}, check your inbox or spam folder to reset your password"
            return MessageOut(message=response)
        if not user.verify:
            response = f"Account not verified, check your inbox or spam folder to verify your account"
            return MessageOut(message=response)
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user, contact support"
            )
        #batch expire existing otp if any
        await session.execute(
            update(OTP)
            .where(and_(OTP.user_id == user.id, OTP.status.in_(["Pending", "Available"])))
            .values(
                status="Expired",
                expires_at=datetime.now(timezone.utc)
            )
        )
        await session.commit()
        # generate otp
        otp = await generate_otp()
        otp_expires_at = datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)
        # store otp in db
        new_otp = OTP(
            email=user.email,
            otp_code=otp,
            user_id=user.id,
            expires_at=otp_expires_at
        )
        session.add(new_otp)
        await session.commit()
        await session.refresh(new_otp)
        # send otp email
        backgroundtask.add_task(
            send_otp_email,
            email=user.email,
            otp=otp,
            username=user.first_name
        )
        response = f"An OTP has been sent to {data.email}, check your inbox or spam folder to reset your password"
        return MessageOut(message=response)
    except HTTPException as Httpexc:
        await session.rollback()
        raise Httpexc

