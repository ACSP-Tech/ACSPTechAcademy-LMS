# app/routes/keepalive.py
from fastapi import APIRouter, Header, HTTPException, status, Depends
from sqlalchemy import text
from ..database_setup import get_db
from ..sec import KEEP_ALIVE_TOKEN

router = APIRouter(tags=["Keep Alive"])

@router.post("/internal/keepalive")
async def keepalive(x_token: str = Header(None), session=Depends(get_db)):
    if x_token != KEEP_ALIVE_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    await session.execute(text("SELECT 1"))
    return {"ok": True}

# Cron-job.org keep-alive
@router.get("/cron")
async def cron_job():
    return {"status": "cron triggered"}