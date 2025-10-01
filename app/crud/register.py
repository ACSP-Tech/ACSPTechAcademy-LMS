from ..model.lms_tables import Users
from fastapi import HTTPException, status
from sqlmodel import select, func
from ..utils.hash_password import password_hash
from ..utils.payload import encode_token

async def user_register(data, session, backgroundtask):
    try:
        #avoid duplicate
        statement = select(Users).where(Users.email == data.email)
        result = await session.execute(statement)
        user_email = result.scalars().first()
        if user_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email {data.email} already registered"
            )
        statement = select(Users).where(Users.phone_number == data.phone_number)
        result = await session.execute(statement)
        user_email = result.scalars().first()
        if user_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Phone Number {data.phone_number} already registered"
            )
        #hash password
        hash_password = await password_hash(data.password)
        # role auto seeding
        statement_role = select(func.count()).select_from(Users)
        result = await session.execute(statement_role)
        user_role = result.scalar_one()
        user_role = "superadmin" if user_role == 0 else "user"
        #add user
        new_user = Users(
            email = data.email,
            first_name = data.first_name,
            last_name = data.last_name,
            hashed_password = hash_password,
            phone_number = data.phone_number,
            role = user_role
        )
        session.add(new_user)

        payload = {
            "email": data.email,
            "first_name": data.first_name,
            "phone_number": data.phone_number,
            "type": "email_verification"
        }
        email_token = await encode_token(payload)

    except HTTPException as Httpexc:
        await session.rollback()
        raise Httpexc