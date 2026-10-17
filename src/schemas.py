# Some part of validation models below were suggested by an AI agent:

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from pydantic_core import PydanticCustomError


# --- Request Models ---
class RegisterInput(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("name")
    @classmethod
    def name_length(cls, v):
        v = v.strip()
        if not 2 <= len(v) <= 100:
            raise PydanticCustomError(
                "name_length",
                "Name must be between 2 and 100 characters.",
            )
        return v

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v):
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def password_length(cls, v):
        v = v.strip()
        if not 8 <= len(v) <= 128:
            raise PydanticCustomError(
                "password_length",
                "Password must be between 8 and 128 characters.",
            )
        return v

    @model_validator(mode="after")
    def passwords_must_match(self):
        if self.password != self.confirm_password:
            raise PydanticCustomError(
                "password_mismatch",
                "Passwords do not match",
            )
        return self


class LoginInput(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def clean_email(cls, v):
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def password_length(cls, v):
        v = v.strip()
        if not 8 <= len(v) <= 128:
            raise PydanticCustomError(
                "password_length",
                "Password must be between 8 and 128 characters.",
            )
        return v


class EventCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)


class CheckInInput(BaseModel):
    attendee_name: str = Field(min_length=2, max_length=100)
    email: EmailStr


class AttendanceOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attendee_name: str
    email: EmailStr


# --- Response Models ---
class OrganizerOut:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
