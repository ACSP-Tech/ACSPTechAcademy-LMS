import cloudinary.uploader
from ..utils import decode_token
from ..model.lms_tables import Users, BlackList
from fastapi import HTTPException, status
from sqlmodel import select, and_
from sqlalchemy.orm import defer
from ..schema.register import MessageOut
from ..utils.hash_password import password_hash, password_verify
from ..utils.payload import encode_email_token
from ..utils.background_email import send_verification_email

from decouple import config
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME"),
    api_key=config("CLOUDINARY_API_KEY"),
    api_secret=config("CLOUDINARY_API_SECRET")
)


async def edit_current_user(firstname, lastname, user_gender, profile_image, country, session, token):
    try:
        #get payload from token
        payload = await decode_token(token)
        user_id = payload.get("id")
        user_email = payload.get("email")
        #get user from db
        user_statement = select(Users).where(and_(Users.id == user_id, Users.email == user_email))
        result = await session.execute(user_statement)
        user = result.scalars().first()
        #Track changes to be made
        changes = False
        if firstname is not None:
            user.first_name = firstname
            changes = True
        if lastname is not None:
            user.last_name = lastname
            changes = True
        if user_gender is not None:
            user.gender = user_gender
            changes = True
        if country is not None:
            user.country = country
            changes = True
        if profile_image and profile_image.filename:
            # Validate file type
            allowed_extensions = {"png", "jpg", "jpeg"}
            file_ext = profile_image.filename.split(".")[-1].lower()
            
            if file_ext not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
                )
            # Validate content type
            if profile_image.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Invalid image format. Only PNG, JPG and JPEG are allowed.")
            # Validate file size (max 5MB)
            # Read file content
            await profile_image.seek(0)
            image_contents = await profile_image.read()
            
            # Check file size (5MB limit)
            max_size = 5 * 1024 * 1024  # 5MB
            if len(image_contents) > max_size:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File too large. Maximum size is 5MB"
                )
            # Delete old image if exists
            if user.profile_public_id:
                try:
                    cloudinary.uploader.destroy(user.profile_public_id)
                except Exception as e:
                    print(f"Failed to delete old image: {e}")
            # Upload to Cloudinary
            try:
                image_upload = cloudinary.uploader.upload(
                    image_contents,
                    folder=f"lms/profiles",
                    public_id=f"user_{user_id}",
                    resource_type="image",
                    overwrite=True,
                    transformation=[
                        {'width': 500, 'height': 500, 'crop': 'fill', 'gravity': 'face'},
                        {'quality': 'auto'},
                        {'fetch_format': 'auto'}
                    ]
                )
                
                user.profile_picture = image_upload['secure_url']
                user.profile_public_id = image_upload['public_id']
                changes = True
                
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to upload image: {str(e)}"
                )  
        # Check if any changes were made
        if not changes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )
        # Save changes to database
        session.add(user)
        await session.commit()
        await session.refresh(user)
        response = "User profile updated successfully"
        return MessageOut(message=response)
    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )   
        
async def user_delete_profile_picture(session, token):
    try:
        #get payload from token
        payload = await decode_token(token)
        user_id = payload.get("id")
        user_email = payload.get("email")
        #get user from db
        user_statement = select(Users).where(and_(Users.id == user_id, Users.email == user_email))
        result = await session.execute(user_statement)
        user = result.scalars().first()
        #raise error if user not found
        if not user.profile_public_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No profile picture found"
            )
        try:
            cloudinary.uploader.destroy(user.profile_public_id)
        except Exception as e:
            print(f"Failed to delete profile image: {e}")
        user.profile_picture = None
        user.profile_public_id = None
        # commit changes
        await session.commit()
        await session .refresh(user)
        response = "User profile picture deleted successfully"
        return MessageOut(message=response)
    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete profile: {str(e)}"
        )
    
async def get_current_user(session, token):
    try:
        #get payload from token
        payload = await decode_token(token)
        user_id = payload.get("id")
        user_email = payload.get("email")
        #get user from db
        user_statement = select(Users).options(defer(Users.hashed_password), 
                                                defer(Users.sub_limit), 
                                                defer(Users.sub_deny_count), 
                                                defer(Users.profile_public_id)).where(and_(Users.id == user_id, 
                                                                                           Users.email == user_email))
        result = await session.execute(user_statement)
        user = result.scalars().first()
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        )
    
async def change_password(data, session, token):
    try:
        #get payload from token
        payload = await decode_token(token)
        user_id = payload.get("id")
        user_email = payload.get("email")
        #get user from db
        user_statement = select(Users).where(and_(Users.id == user_id, Users.email == user_email))
        result = await session.execute(user_statement)
        user = result.scalars().first()
        #verify old password
        verify = await password_verify(data.old_password, user.hashed_password)
        if not verify:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid old password"
            )
        #hash new password
        hash_new_password = await password_hash(data.new_password)
        user.hashed_password = hash_new_password
        # commit changes
        await session.commit()
        await session.refresh(user)
        response = "Password changed successfully"
        return MessageOut(message=response)
    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )

async def edit_current_user_email(data, backgroundtask, token, session):
    try:
        #get payload from token
        payload = await decode_token(token)
        id = payload.get("id")
        old_email = payload.get("email")
        #get user from db
        user_statement = select(Users).where(and_(Users.id == id, Users.email == old_email))
        result = await session.execute(user_statement)
        user = result.scalars().first()
        #check if email already exists
        email_statement = select(Users).where(Users.email == data.email)
        email_result = await session.execute(email_statement)
        email_user = email_result.scalars().first()
        if email_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Enter a different email, {data.email} already exists"
            )
        user.email = data.email
        user.verify = False
        # commit changes
        await session.commit()
        await session.refresh(user)

        new_blacklist = BlackList(black_token=token, user_id=id)
        session.add(new_blacklist)
        await session.commit()
        await session.refresh(new_blacklist)
 
        payload = {
            "email": data.email,
            "first_name": data.first_name,
            "phone_number": data.phone_number,
            "type": "email_verification"
        }
        email_token = await encode_email_token(payload)
        backgroundtask.add_task(
            send_verification_email,
            email=data.email,
            token=email_token,
            username=data.first_name
        )
        response = "User email updated successfully, Verification email has been sent. Kindly verify your new email and login again"
        return MessageOut(message=response)
    except HTTPException:
        await session.rollback()
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update email: {str(e)}"
        )