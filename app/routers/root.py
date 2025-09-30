from fastapi import APIRouter

router = APIRouter()

# Render liveness check
@router.get("/")
async def root():
    return {"app_name": "ACSP Learning Management Software",}