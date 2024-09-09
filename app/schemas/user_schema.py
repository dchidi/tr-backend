from pydantic import BaseModel, EmailStr


# Base schema for user
class UserBase(BaseModel):
    username: str
    email: EmailStr


# Schema for creating a new user (input validation)
class UserCreate(UserBase):
    password: str


# Schema for retrieving a user (output, with an ID)
class User(UserBase):
    id: str  # MongoDB ObjectId will be stored as a string

    class Config:
        orm_mode = True
