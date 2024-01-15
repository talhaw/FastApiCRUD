from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    is_active: Optional[bool] = False


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: UUID


class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
