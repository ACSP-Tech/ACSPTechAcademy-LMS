import uuid
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime, date
from pydantic import EmailStr, field_validator
from sqlalchemy import String, func, DateTime, Integer, desc, Index
from typing import List, Optional

class Users(SQLModel, table=True):
    id: str = Field(
    default_factory=lambda: str(uuid.uuid4()),
    sa_column=Column(String(36), primary_key=True, nullable=False)
    )
    email: EmailStr = Field(
        sa_column=Column(String, unique=True, nullable=False, index=True)
    )
    hashed_password: str = Field(
        sa_column=Column(String, nullable=False))
    first_name: str = Field(
        sa_column=Column(String, nullable=False))
    last_name: str = Field(
        sa_column=Column(String, nullable=False))
    phone_number: str = Field(
        sa_column=Column(String, nullable=False))
    gender: str = Field(
        sa_column=Column(String, nullable=False))
    course:str = Field(default="na",
        sa_column=Column(String, nullable=False, index=True))
    role: str = Field(
        sa_column=Column(String, nullable=False, index=True))
    is_active: bool = Field(default=True, index=True)
    verify: bool = Field(default=False, index=True)
    version: int = Field(default= 0, sa_column=Column(Integer, nullable=False, index=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    sub_limit: int = Field(default= 1, sa_column=Column(Integer, nullable=False, index=True))
    current_stage: int = Field(default= 0, sa_column=Column(Integer, nullable=False, index=True))
    sub_deny_count:int = Field(default= 0, sa_column=Column(Integer, nullable=False, index=True))

    @field_validator("course", "role", mode = "before")
    def normalize_fields(cls, value):
        if isinstance(value, str):
            return value.strip().lower()
        return value