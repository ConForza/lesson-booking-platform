from pydantic import BaseModel, EmailStr


class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    email: str
    is_active: bool

class User(BaseModel):
    email: str
    password: str
    is_active: bool
