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
    course: str = Field(default="Na",
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

    #defining relationships
    tasks: List["Task"] = Relationship(back_populates="users")
    blacklists: List["BlackList"] = Relationship(back_populates="users")
    Usersubscriptions: List["UserSubscription"] = Relationship(back_populates="users")
    subscriptions: List["Subscription"] = Relationship(back_populates="users")
    classrooms: List["ClassRoom"] = Relationship(back_populates="users")
    studenttasks: List["StudentTask"] = Relationship(back_populates="users")

class BlackList(SQLModel, table=True):
    black_token: str = Field(primary_key=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    #foreign keys
    user_id: str = Field(foreign_key="users.id")

    #defining relationships
    users: Optional["Users"] = Relationship(back_populates="blacklists")

class Task(SQLModel, table=True):
    task_id: str = Field(
    default_factory=lambda: str(uuid.uuid4()),
    sa_column=Column(String(36), primary_key=True, nullable=False))
    task_name: str = Field(sa_column=Column(String, nullable=False, index=True))
    stage: int = Field(sa_column=Column(Integer, nullable=False, index=True)) 
    task_details: str = Field(sa_column=Column(String, nullable=False, index=True))
    due_date: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    version: int = Field(default= 0, sa_column=Column(Integer, nullable=False, index=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    status: str = Field(default="Pending", sa_column=Column(String, nullable=False, index=True))
    course: str = Field(default="Data Analysis", sa_column=Column(String, nullable=False, index=True))
    level: str = Field(default="Beginner", sa_column=Column(String, nullable=False, index=True))
    #foreign key
    user_id: str = Field(foreign_key="users.id")
    #relationships
    users: Optional["Users"] = Relationship(back_populates="tasks")
    #define relationships
    classrooms: List["ClassRoom"] = Relationship(back_populates="task")
    studenttasks: List["StudentTask"] = Relationship(back_populates="task")
    #field_validator if need be

class StudentTask(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), sa_column=Column(String(36), primary_key=True, nullable=False))
    email: str = Field(sa_column=Column(String, nullable=False, index=True))
    status: str = Field(default="Submitted", sa_column=Column(String, nullable=False, index=True))
    submission_link: str = Field(sa_column=Column(String, nullable=False, index=True))
    score: int = Field(sa_column=Column(Integer, nullable=False, index=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    #foreign key
    user_id: str = Field(foreign_key="users.id")
    task_id: str = Field(foreign_key="task.task_id")
    #relationships
    users: Optional["Users"] = Relationship(back_populates="studenttasks")
    task: Optional["Task"] = Relationship(back_populates="studenttasks")


class ClassRoom(SQLModel, table=True):
    class_id: str = Field(default_factory=lambda: str(uuid.uuid4()), sa_column=Column(String(36), primary_key=True, nullable=False))
    video_url: str = Field(sa_column=Column(String, nullable=False, index=True))
    video_public_id: str = Field(sa_column=Column(String, nullable=False, index=True))
    view_count: int = Field(sa_column=Column(Integer, nullable=False, index=True))
    duration: int = Field(sa_column=Column(Integer, nullable=False, index=True))
    thumbnail_url: str = Field(sa_column=Column(String, nullable=False, index=True))
    folder: str = Field(sa_column=Column(String, nullable=False, index=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False))
    #foreign key
    user_id: str = Field(foreign_key="users.id")
    task_id: str = Field(foreign_key="task.task_id")
    #relationships 
    users: Optional["Users"] = Relationship(back_populates="classrooms") #one to many
    task: Optional["Task"] = Relationship(back_populates="classrooms") #one to one

class Subscription(SQLModel, table=True):
    sub_id: str = Field(default_factory=lambda: str(uuid.uuid4()), sa_column=Column(String(36), primary_key=True, nullable=False))
    sub_details: str = Field(sa_column=Column(String, nullable=False))
    acc_details: str = Field(sa_column=Column(String, nullable=False))
    status: str = Field(default="Active", sa_column=Column(String, nullable=False, index=True))
    version: int = Field(sa_column=Column(Integer, nullable=False, index=True))
    course: str = Field(sa_column=Column(String, nullable=False, index=True))
    #foreign key
    user_id: str = Field(foreign_key="users.id")
    #relationships 
    users: Optional["Users"] = Relationship(back_populates="subscriptions")
    #defining relationships
    usersubscriptions: List["UserSubscription"] = Relationship(back_populates="subscription")

class UserSubscription(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), sa_column=Column(String(36), primary_key=True, nullable=False))
    status: str = Field(default="Pending", sa_column=Column(String, nullable=False, index=True))
    payment_url: str = Field(sa_column=Column(String, nullable=False, index=True))
    payment_public_id: str = Field(sa_column=Column(String, nullable=False, index=True))
    total_pages: int = Field(default= 0, sa_column=Column(Integer, nullable=False, index=True))
    filename: str = Field(sa_column=Column(String, nullable=False, index=True))
    filetype: str = Field(sa_column=Column(String, nullable=False, index=True))
    sub_status: str = Field(default="Inactive", sa_column=Column(String, nullable=False, index=True))
    #foreign key
    user_id: str = Field(foreign_key="users.id")
    sub_id: str = Field(foreign_key="subscription.sub_id")
    #relationships 
    users: Optional["Users"] = Relationship(back_populates="usersubscriptions")
    subscription: Optional["Subscription"] = Relationship(back_populates="usersubscriptions")