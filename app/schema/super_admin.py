from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status

class UserResponse(BaseModel):
    model_config = {"from_attributes": True}
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    course: str
    role: str
    is_active: bool
    verify: bool
    num_verify: bool
    version: int
    created_at: datetime
    updated_at: datetime
    current_stage: int
    profile_picture: Optional[str] = None
    country: Optional[str] = None
    gender: Optional[str] = None
    sub_limit: int
    sub_deny_count: int


class AutoFil(BaseModel):
    users: List[UserResponse]
    total: int
    limit: int

class Fil(BaseModel):
    role: Optional[str]
    course: Optional[str]
    other: Optional[str]
    version: Optional[int]

class StringFil(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    size: int
    pages: int
    filter_applied: Dict[str, Any]

class UserUpdateItem(BaseModel):
    """Schema for updating user information"""
    user_id: str = Field(..., description="ID of the user to update")
    role: Optional[str] = Field(None, min_length=1, max_length=50, description="New role (user, admin)")
    is_active: Optional[bool] = Field(None, description="Active status (true/false)")
    
    @field_validator('role', 'is_active')
    @classmethod
    def at_least_one_field(cls, v, info):
        """Ensure at least one field is provided"""
        values = info.data
        if v is None and all(val is None for val in values.values()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"At least one field (role or is_active) must be provided")
        return v
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        """Validate role is one of the allowed values"""
        if v is not None:
            allowed_roles = ['user', 'admin']
            if v.lower() not in allowed_roles:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Role must be one of: {', '.join(allowed_roles)}")
        return v

class UserUpdateSchema(BaseModel):
    """Schema for batch updating users"""
    users: List[UserUpdateItem] = Field(..., min_length=1, description="List of users to update")    


class UserEditResult(BaseModel):
    """Single user edit result"""
    user_id: str
    success: bool
    message: str
    user: Optional[UserResponse] = None


class UserEdit(BaseModel):
    """Response model for batch user update"""
    total_processed: int
    successful: int
    failed: int
    results: List[UserEditResult]