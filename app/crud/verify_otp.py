from ..model.lms_tables import OTP
from sqlmodel import select, and_
from fastapi import HTTPException, status
from datetime import datetime, timezone
from ..schema.register import MessageOut

async def user_verify_otp(data, session):
    """Verify user OTP"""
    try:
        user_email = data.email
        otp_code = data.otp
        # Check if valid forget email request exists
        statement = select(OTP).where(and_(OTP.email == user_email, OTP.status == "Pending"))
        result = await session.execute(statement)
        otp_entry_check = result.scalars().first()
        if not otp_entry_check:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid otp request, please request a new otp"
            )
        # Check if OTP matches
        if otp_entry_check.otp != otp_code:
            otp_entry_check.attempts += 1
            await session.commit()
            await session.refresh(otp_entry_check)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect OTP, try again"
            )
        #if otp has expired
        if otp_entry_check.expires_at < datetime.now(timezone.utc):
            otp_entry_check.status = "Expired"
            otp_entry_check.attempts += 1
            await session.commit()
            await session.refresh(otp_entry_check)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )
        if otp_entry_check.attempts >= 5:
            otp_entry_check.status = "Expired"
            await session.commit()
            await session.refresh(otp_entry_check)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Maximum OTP attempts exceeded. Please request a new OTP."
            )
        # Mark OTP as used
        otp_entry_check.status = "Available"
        otp_entry_check.attempts += 1
        otp_entry_check.verified = True
        await session.commit()
        await session.refresh(otp_entry_check)
        return MessageOut(message="OTP verified successfully")
    except HTTPException as Httpexc:
        await session.rollback()
        raise Httpexc
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
