from datetime import datetime
from pydantic import BaseModel
from .model import UserTypeEnum


class UserBase(BaseModel):
    username: str
    email: str
    birthday: datetime
    user_type: UserTypeEnum


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class TokenData(User):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str
