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
    # Từ 12/11/2026 app dùng email + mã 6 số (hiệu lực 5 phút, sai 10 lần thì huỷ mã) thay cho
    # token dài. Độ mạnh mật khẩu và việc chấm mã do backend app làm — web chỉ chuyển tiếp.
    email: EmailStr
    code: str = Field(pattern=r"^\s*\d{6}\s*$")
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
