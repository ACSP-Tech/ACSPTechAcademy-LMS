from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, File, BackgroundTasks
from ..database_setup import get_db
from ..dep.authen import superadmin_auth
from ..crud.super_admin import get_all_users
from ..utils.pagination import UserParams
from ..schema.super_admin import UserResponse
from fastapi_pagination import Page

router = APIRouter(prefix="/superadmin", tags=["User Manager CRUD - superadmin"])

@router.get("/users", response_model=Page[UserResponse],  status_code=status.HTTP_200_OK)
async def view_all_users_profile(params: UserParams = Depends(), session = Depends(get_db), token = Depends(superadmin_auth)):
    """
    Retrieve paginated list of users (excludes superadmins).
    
    - No request body needed.
    - Returns all users information with pagination.
    - Args:
        - total  = the total number of results in the db.
        - size = number of result per page, default to 10, max 50, min 1.
        - page = current page, default to page 1.
        - pages = total number of pages (default to (total divided by size)).
    - Superadmin authenticated route
    - NB: Passwords and sensitive info are excluded from the response.
    - *NB: gender, country and profile_picture fields could return null if not set by user*.
    """
    try:
        # Placeholder for actual implementation
        return await get_all_users(params, session, token)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))