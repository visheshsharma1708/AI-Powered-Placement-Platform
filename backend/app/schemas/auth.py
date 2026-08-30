from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: str
    full_name: str
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse