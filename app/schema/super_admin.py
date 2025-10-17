from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

class UserResponse(BaseModel):
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