from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.core.permissions import Role


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: Role = Role.CITIZEN


class UserRead(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
