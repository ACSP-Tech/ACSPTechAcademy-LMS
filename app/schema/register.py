from ..utils.general import StrictBaseModel as BaseModel
from pydantic import EmailStr, Field, field_validator
from typing import Annotated
import re

class Register(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=15, description="must include at least 1 letter(either uppercase or lower), 1 integer, and 1 special charater")]
    first_name: Annotated[str, Field(min_length=3, max_length=15, description="no space, 3 to 15 character, only string")]
    last_name: Annotated[str, Field(min_length=3, max_length=15, description="no space, 3 to 15 character, only string")]
    phone_number: Annotated[str, Field(min_length=2, max_length=15, description="Must be a valid phone number start with phone number e.g +23490xxxxxxxx or +447911123456")]
    #field_validator to enforce description
    @field_validator("password")
    def validate_password(cls, v:str) ->str:
        v = v.strip()
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("password must contain at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[^A-Za-z0-9]", v):
            raise ValueError("Password must contain at least one special character")
        return v
    @field_validator("first_name", "last_name")
    def validate_names(cls, v: str) -> str:
        v = v.strip()
        if not re.fullmatch(r"[A-Za-z]{3,15}", v):
            raise ValueError("Name must be 3 to 15 alphabetic characters with no spaces")
        return v.title()
    @field_validator("phone_number")
    def validate_phone_number(cls, v: str) -> str:
        v = v.strip()
        # E.164 regex: starts with +, then 1-15 digits
        pattern = re.compile(r'^\+[1-9]\d{1,14}$')
        if not pattern.match(v):
            raise ValueError("Phone number must be in valid E.164 format (e.g., +14155552671)")
        return v


class MessageOut(BaseModel):
    message: str