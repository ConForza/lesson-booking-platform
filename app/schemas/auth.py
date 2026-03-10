from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    is_active: bool

class User(BaseModel):
    email: str
    password: str
    is_active: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
