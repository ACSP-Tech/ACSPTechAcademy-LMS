from ..utils.general import StrictBaseModel as BaseModel
from pydantic import EmailStr, field_validator, Field
import re
from typing import Annotated
class ForgotPassword(BaseModel):
    email: EmailStr
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

class verifyOTP(BaseModel):
    email: EmailStr
    otp: str
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

class Reset(BaseModel):
    email: EmailStr
    otp: str
    new_password: Annotated[str, Field(min_length=8, max_length=15, description="must include at least 1 letter(either uppercase or lower), 1 integer, and 1 special charater")]
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()
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