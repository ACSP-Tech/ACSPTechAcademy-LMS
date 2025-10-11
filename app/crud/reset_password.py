from ..model.lms_tables import Users, OTP
from sqlmodel import select, and_, distinct
from ..schema.register import MessageOut  
from fastapi import HTTPException, status
from ..utils.hash_password import password_hash
from datetime import datetime, timezone

async def user_reset_password(data, session):
    """Reset user password"""
    try:
        user_otp = data.otp
        user_email = data.email
        new_password = data.new_password
        # Build subquery to get distinct book_ids for user with Returned/Expired status
        otp_stmt = select(OTP).where(
                and_(
                    OTP.email == user_email,
                    OTP.status == "Available",
                    OTP.verified == True,
                    OTP.otp_code == user_otp
                )
            )
        otp_result = await session.execute(otp_stmt)
        otp_entry = otp_result.first()
        if not otp_entry:
            response = "Password reset successfully! You can now login with your new password."
            return MessageOut(
                message=response
            )
        
        #if otp has expired
        if otp_entry.expires_at < datetime.now(timezone.utc):
            otp_entry.status = "Expired"
            await session.commit()
            await session.refresh(otp_entry)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )
        # Main query - join Book with the subquery
        stmt = select(Users).where(Users.id == otp_entry.user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user, contact support"
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user, contact support"
            )
        if not user.verify:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account not verified, check your inbox or spam folder to verify your account first"
            )
        # update otp entry as verified
        otp_entry.status = "Used"
        await session.commit()
        await session.refresh(otp_entry)

        # hash new password
        hashed_password = await password_hash(new_password)
        # update user password
        user.hashed_password = hashed_password
        # save to db
        await session.commit()
        await session.refresh(user)

        response = "Password reset successfully! You can now login with your new password."
        return MessageOut(
            message=response
        )
    except HTTPException as Httpexc:
        await session.rollback()
        raise Httpexc