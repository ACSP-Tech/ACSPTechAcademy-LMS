from ..utils.general import StrictBaseModel as BaseModel
from pydantic import EmailStr, field_validator

class LoginUser(BaseModel):
    email: EmailStr
    password: str
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

class LogOut(BaseModel):
    role: str
    first_name: str
    token: str
    token_type: str