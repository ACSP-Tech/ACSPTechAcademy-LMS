from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum
import re
from datetime import datetime
from pydantic import EmailStr
from typing import Annotated

class GenderEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-Binary"
    PREFER_NOT_TO_SAY = "Prefer not to say"
    OTHER = "Other"
    none = ""
    

class UserProfileResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str]
    gender: Optional[str]
    country: Optional[str]
    profile_picture: Optional[str]
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()
    @field_validator("first_name", "last_name")
    def validate_names(cls, v: str) -> str:
        v = v.strip()
        if not re.fullmatch(r"[A-Za-z]{3,15}", v):
            raise ValueError("Name must be 3 to 15 alphabetic characters with no spaces")
        return v.title()
    
class ProfileResponse(BaseModel):
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
    profile_picture: Optional[str]
    country: Optional[str]
    gender: Optional[str]

class ChangePassword(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=8, max_length=15, description="must include at least 1 letter(either uppercase or lower), 1 integer, and 1 special charater")]
    @field_validator("new_password")
    def validate_password(cls, v:str) ->str:
        v = v.strip()
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one special character")
        return v

class UserEmail(BaseModel):
    email: EmailStr
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()
    
class UserPhone(BaseModel):
    phone_number: str
    @field_validator("phone_number")
    def validate_phone_number(cls, v: str) -> str:
        v = v.strip()
        # E.164 regex: starts with +, then 1-15 digits
        pattern = re.compile(r'^\+[1-9]\d{1,14}$')
        if not pattern.match(v):
            raise ValueError("Phone number must be in valid E.164 format (e.g., +14155552671)")
        return v
    
    