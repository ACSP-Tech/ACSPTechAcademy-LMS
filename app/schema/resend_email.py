from ..utils.general import StrictBaseModel as BaseModel
from pydantic import EmailStr, field_validator

class Resend(BaseModel):
    email: EmailStr
    @field_validator("email")
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()