# The validation models below were suggested by an AI agent:

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class EventCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)


class CheckInInput(BaseModel):
    attendee_name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class AttendanceOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attendee_name: str
    email: EmailStr
