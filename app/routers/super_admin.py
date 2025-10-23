from fastapi import APIRouter, Depends, HTTPException, status, Query
from ..database_setup import get_db
from ..dep.authen import superadmin_auth
from ..crud.super_admin import get_all_users, search_user, search_query_result, edit_user
from ..utils.pagination import UserParams
from ..schema.super_admin import UserResponse, AutoFil, StringFil, UserUpdateSchema, UserEdit
from fastapi_pagination import Page
from typing import Annotated, Optional

router = APIRouter(prefix="/superadmin", tags=["User Manager- superadmin"])

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

@router.get("/user-search", response_model=AutoFil, status_code=status.HTTP_200_OK)    
async def auto_complete_search_endpoint(q: Annotated[str, Query(min_length=1, max_length=50, description="User text to search")],
                         limit: int = Query(default=20, ge=1, le=20, description="Max results to return"), 
                         session = Depends(get_db), token = Depends(superadmin_auth)):
    """
    step 1/2 : Autocomplete Endpoint, automatically populate batch edit user info based on the user email, or firstname typed
    - limit set to  max 20 parameters, min 1,  default 20.
    - return all user info 
    - case insensitive
    - the search query (autocomplete on email, firstname, lastname)
        - min_length=2, max_length=50
    - Return empty results for autocomplete if no result found
    - So the flow:
        - GET .../search?q=john - Returns matching users
        - User selects → form populated with user data
        - Admin edits role/is_active
        - PATCH .../edit-users- Saves the changes
    - Superadmin authenticated route
    - NB: Passwords and sensitive info are excluded from the response.
    - *NB: gender, country and profile_picture fields could return null if not set by user*.
    """
    try:
        return await search_user(q, limit, session)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    

@router.get("/dynamic-search", response_model=StringFil, status_code=status.HTTP_200_OK)
async def all_user_search_endpoint(
    page: int = Query(default=1, ge=1, description="Page number (starts from 1)"),
    size: int = Query(default=20, ge=1, le=50, description="Number of record per page to return"),
    role: Optional[str] = Query(None, min_length=1, max_length=50, description="search specfically by user role (user, admin)"), 
    course: Optional[str] = Query(None, description="search specifically by course"),
    other: Optional[str] = Query(None, description="search the entire dataframe for a match"),
    version: Optional[int] = Query(None, description="search specifically by version"),
    session = Depends(get_db), token = Depends(superadmin_auth)):
    """
    Endpoint to get all strings that match with filtering
    - Args:
        - takes 6 query parameters
            - all is optional
        - case insensitive
        - pagination exist 
            - total  = the total number of results in the db.
            - size = number of result per page, default to 10, max 50, min 1.
            - page = current page, default to page 1.
            - pages = total number of pages (default to (total divided by size)).
    - Superadmin authenticated route
    - NB: Passwords and sensitive info are excluded from the response.
    - *NB: gender, country and profile_picture fields could return null if not set by user*.
    """
    try:
        return await search_query_result(page, size, role, course, other, version, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.patch("/edit-users", response_model=UserEdit, status_code=status.HTTP_200_OK)
async def update_user(
    update_data: UserUpdateSchema,
    session = Depends(get_db),
    token = Depends(superadmin_auth)
):
    """
    Endpoint to Update user information (role, is_active) 
        - change user role 
        - block user is_active(false)
        - activate user is_active(fasle)
    - take UserUpdateSchema body paramters. a list of user info, user_id must and at least one field to update between role and is_active
    """ 
    try:
        return await edit_user(update_data, session)
    except HTTPException as httpexc:
        raise httpexc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )