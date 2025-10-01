from fastapi import APIRouter, Response

router = APIRouter()

# Render liveness check
@router.get("/")
async def root():
    return {"app_name": "ACSP Learning Management Software",}

@router.head("/")
async def root_head():
    return Response(status_code=200)