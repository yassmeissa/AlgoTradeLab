"""User schemas"""

from pydantic import BaseModel, EmailStr, model_validator
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """User creation schema"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema"""
    email: Optional[str] = None
    username: Optional[str] = None
    password: str
    
    @model_validator(mode='after')
    def check_email_or_username(self):
        """Ensure at least email or username is provided"""
        if not self.email and not self.username:
            raise ValueError('Either email or username must be provided')
        return self
        if self.email and self.username:
            # If both provided, clear one (prioritize username)
            self.email = None


class UserUpdate(BaseModel):
    """User update schema"""
    full_name: Optional[str] = None
    username: Optional[str] = None


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    username: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
