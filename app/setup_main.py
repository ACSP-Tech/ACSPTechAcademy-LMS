from fastapi.middleware.cors import CORSMiddleware
from .model.lms_tables import OTP
from sqlmodel import select, update, and_
from datetime import datetime, timezone, timedelta
import asyncio
from .database_setup import engine, AsyncSession

def configure_cors(app):
    """Configure CORS middleware for the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

async def cleanup_otp():
    """Periodic cleanup task that marks expired OTPs as 'Expired' daily at 2 AM."""
    try:
        while True:
            async with AsyncSession(engine) as session:
                # Delete OTP entries older than 15 minutes
                now = datetime.now(timezone.utc) 
                await session.execute(update(OTP)
                    .where(OTP.expires_at < now).values(status="Expired"))
                await session.commit()
            tomorrow_2am = (now + timedelta(days=1)).replace(hour=2, minute=0, second=0, microsecond=0)
            sleep_seconds = (tomorrow_2am - now).total_seconds()
            #print(f"{sleep_seconds}")     
            await asyncio.sleep(sleep_seconds)
    except asyncio.CancelledError:
        # Clean shutdown
        return