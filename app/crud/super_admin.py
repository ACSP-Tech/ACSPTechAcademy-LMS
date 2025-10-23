from ..utils.payload import decode_token
from ..model.lms_tables import Users
from fastapi import HTTPException, status
from sqlmodel import select, or_, and_, func
from sqlalchemy.orm import defer
from fastapi_pagination.ext.sqlalchemy import paginate
from ..schema.super_admin import AutoFil, UserEditResult, UserEdit, StringFil, Fil
from datetime import datetime
from math import ceil

async def get_all_users(params, session, token):
    try:
        statement = select(Users).options(defer(Users.hashed_password), 
                                                defer(Users.profile_public_id)).where(Users.role != "superadmin").order_by(Users.created_at.desc())
        return await paginate(session, statement, params)
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

async def search_user(q, lim, session):
    try:
        query = q.strip()
        statement = select(Users).options(defer(Users.hashed_password), 
                                          defer(Users.profile_public_id)).where(or_(
                                            Users.email.ilike(f"%{query}%"),
                                            Users.first_name.ilike(f"%{query}%"),
                                            Users.last_name.ilike(f"%{query}%")
                                          )).limit(lim)
        result = await session.execute(statement)
        all_matching_users = result.scalars().all()
        all_users = AutoFil(
            users = all_matching_users,
            total = len(all_matching_users),
            limit = lim 
        )
        return all_users
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    

async def edit_user(update_data, session):
    """
    Batch update user role and/or is_active status
    """
    try:
        results = []
        successful = 0
        failed = 0
        
        for user_update in update_data.users:
            try:
                # Find the user
                statement = select(Users).where(Users.id == user_update.user_id)
                result = await session.execute(statement)
                user = result.scalar_one_or_none()
                
                if not user:
                    results.append(UserEditResult(
                        user_id=user_update.user_id,
                        success=False,
                        message=f"User with ID {user_update.user_id} not found",
                        user=None
                    ))
                    failed += 1
                    continue
                
                # Track what was updated
                updated_fields = []
                
                # Update role if provided
                if user_update.role is not None:
                    user.role = user_update.role.lower()
                    updated_fields.append("role")
                
                # Update is_active if provided
                if user_update.is_active is not None:
                    user.is_active = user_update.is_active
                    updated_fields.append("is_active")
                
                # Update the updated_at timestamp
                user.updated_at = datetime.utcnow() 
                
                # Commit changes for this user
                await session.commit()
                await session.refresh(user)
                
                # Create success message
                fields_str = " and ".join(updated_fields)
                message = f"User {fields_str} updated successfully"
                
                results.append(UserEditResult(
                    user_id=user_update.user_id,
                    success=True,
                    message=message,
                    user=user
                ))
                successful += 1
                
            except Exception as exc:
                await session.rollback()
                results.append(UserEditResult(
                    user_id=user_update.user_id,
                    success=False,
                    message=f"Error updating user: {str(exc)}",
                    user=None
                ))
                failed += 1
        
        return UserEdit(
            total_processed=len(update_data.users),
            successful=successful,
            failed=failed,
            results=results
        )
    except HTTPException as Httpexc:
        raise Httpexc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    


async def search_query_result(page, size, role, course, other, version, session):
    """
    Dynamic search with pagination across user fields
    """
    try:
        # Calculate offset
        skip = (page - 1) * size
        
        # Build dynamic filters
        filters = []
        
        if role is not None:
            filters.append(Users.role == role)        
        if course:
            filters.append(Users.course.ilike(f"%{course.strip()}%"))
        
        if version is not None:
            filters.append(Users.version == version)
        
        if other is not None:
            # Search across multiple fields for "other" query
            other_query = other.strip()
            filters.append(
                or_(
                    Users.email.ilike(f"%{other_query}%"),
                    Users.first_name.ilike(f"%{other_query}%"),
                    Users.last_name.ilike(f"%{other_query}%"),
                    Users.phone_number.ilike(f"%{other_query}%"),
                    Users.country.ilike(f"%{other_query}%"),
                    Users.gender.ilike(f"%{other_query}%"),
                    Users.role.ilike(f"%{other_query}%"),
                    Users.version.ilike(f"%{other_query}%"),
                    Users.course.ilike(f"%{other_query}%")
                    ))
        
        
        # Get total count
        count_statement = select(func.count()).select_from(Users).where(and_(*filters) if filters else True)
        total_result = await session.execute(count_statement)
        total = total_result.scalar()
        
        filte = Fil(
            role = role,
            course = course,
            other = other,
            version = version
        )
        
        if total == 0:
            return StringFil(
                users=[],
                total=0,
                page=page,
                size=size,
                pages=0,
                filter_applied = filte.model_dump(exclude_none=True)
            )
        
        # Get paginated results
        statement = select(Users).options(
            defer(Users.hashed_password),
            defer(Users.profile_public_id)
        ).where(and_(*filters) if filters else True).order_by(Users.version).offset(skip).limit(size)
        
        result = await session.execute(statement)
        users = result.scalars().all()
        
        # Calculate total pages
        pages = ceil(total / size)

        #getting the filters applied
        filte = Fil(
            role = role,
            course = course,
            other = other,
            version = version
        )
        
        return StringFil(
            users=users,
            total=total,
            page=page,
            size=size,
            pages=pages,
            filter_applied = filte.model_dump(exclude_none=True)
        )
        
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching users: {str(exc)}"
        )