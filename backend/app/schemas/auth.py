from pydantic import BaseModel, EmailStr, Field


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


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    # Độ mạnh mật khẩu do backend app kiểm tra (validate_password_strength) — web chỉ chuyển tiếp.
    token: str = Field(min_length=1, max_length=200)
    new_password: str = Field(max_length=200)
    confirm_password: str = Field(max_length=200)


class MessageResponse(BaseModel):
    message: str


class UserProfileOut(BaseModel):
    id: int
    email: str
    full_name: str | None
    phone_number: str | None = None
    is_admin: bool = False
