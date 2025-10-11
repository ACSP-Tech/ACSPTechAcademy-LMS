from ..utils.general import StrictBaseModel as BaseModel
from pydantic import EmailStr, field_validator

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
    new_password: str
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()