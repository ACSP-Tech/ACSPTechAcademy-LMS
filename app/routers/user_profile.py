from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, File, BackgroundTasks
from ..database_setup import get_db
from ..dep.authen import user_auth
from ..schema.user_profile import UserProfileResponse, GenderEnum, ProfileResponse, ChangePassword, UserEmail, UserPhone
from ..crud.user_profile import edit_current_user, user_delete_profile_picture, get_current_user, change_password, edit_current_user_email, edit_phone_number
from typing import Annotated, Optional
from ..schema.register import MessageOut

router = APIRouter(prefix="/user", tags=["Users Profile CRUD"])

@router.patch("/profile/edit-info", response_model=UserProfileResponse, status_code=status.HTTP_201_OK)
async def edit_user_profile(firstname: Annotated[Optional[str], Form()] = None, 
                            lastname: Annotated[Optional[str], Form()] = None, 
                            user_gender: Annotated[Optional[GenderEnum], Form()] = None,
                            profile_image: Optional[UploadFile] = File(None),
                            country: Annotated[Optional[str], Form()] = None,
                            session = Depends(get_db), 
                            token = Depends(user_auth)):
    """
    Edit user profile details.
    
    **Content-Type: multipart/form-data**
    
    - All fields are optional - only send fields you want to update
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **gender**: Dropdown options (Male, Female, Non-Binary, Prefer not to say, Other)
    - **country**: User's country
    - **profile_image**: Profile picture (PNG/JPEG, max 5MB) - optional
    
    **Note:** Email and phone number cannot be changed here. 
    Use separate verification endpoints for those.
    """
    try:
        return await edit_current_user(firstname, lastname, user_gender, profile_image, country, session, token)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.patch("/profile/delete-picture", response_model=MessageOut, status_code=status.HTTP_201_OK)
async def delete_profile_picture(session = Depends(get_db), token = Depends(user_auth)):
    """
    Delete user's profile picture.
    
    This endpoint removes the user's current profile picture from their account.
    - No request body needed.
    - Returns updated user profile without the profile picture.
    
    **Note:** This action cannot be undone. A default placeholder image will be used after deletion.
    """
    try:
        return await user_delete_profile_picture(session, token)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) 


@router.get("/profile", response_model=ProfileResponse, status_code=status.HTTP_200_OK)
async def get_user_profile(session = Depends(get_db), token = Depends(user_auth)):
    """
    Retrieve the authenticated user's profile information.
    
    - No request body needed.
    - Returns user table information aside from password and sensitive fields.
    """
    try:
        return await get_current_user(session, token)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
@router.patch("/profile/change-password", response_model=MessageOut, status_code=status.HTTP_201_OK)
async def change_user_password(data: ChangePassword, 
                               session = Depends(get_db), 
                               token = Depends(user_auth)):
    """
    Change the authenticated user's password.
    
    - **old_password**: Current password (required)
    - **new_password**: New password (required, min 8 characters with letters and numbers)
    
    **Note:** User must provide their current password to set a new one. 
    Password strength requirements apply to the new password.
    """
    try:
        return await change_password(data, session, token)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
@router.patch("/pofile/edit-email", response_model=MessageOut, status_code=status.HTTP_201_OK)
async def edit_user_email(data:UserEmail, backgroundtask:BackgroundTasks, session = Depends(get_db), token = Depends(user_auth)):
    """
    Edit user email.
    """
    try:
        return await edit_current_user_email(data, backgroundtask, session, token)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    
# @router.post("/profile/verify-phone-number", response_model=MessageOut, status_code=status.HTTP_200_OK)
# async def verify_phone_number(data:VerifyPhone, session = Depends(get_db), token = Depends(user_auth)):
#     """
#     Verify user's phone number with OTP.
#     """
#     try:
#         return await edit_current_user_email(data, session, token)
#     except HTTPException as Httpexc:
#         raise Httpexc
#     except Exception as exc:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    
@router.patch("/pofile/edit-phone-nuber", response_model=MessageOut, status_code=status.HTTP_201_OK)
async def edit_user_email(data:UserPhone, backgroundtask:BackgroundTasks, session = Depends(get_db), token = Depends(user_auth)):
    """
    Edit user email.
    """
    try:
        return await edit_phone_number(data, backgroundtask, session, token)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    

