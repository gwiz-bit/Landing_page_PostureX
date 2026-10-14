from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp_code: str


class ResendOtpRequest(BaseModel):
    email: EmailStr


class MessageResponse(BaseModel):
    message: str


class UserProfileOut(BaseModel):
    id: int
    email: str
    full_name: str | None
    phone_number: str | None = None
    is_admin: bool = False
