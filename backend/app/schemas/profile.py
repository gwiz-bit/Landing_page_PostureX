"""Mirror của `ProfileOut`/`ProfileUpdate` bên backend app
(`backend/app/schemas/profile.py` của repo PostureX) — chỉ 6 trường có cột
DB thật. Web không tự định nghĩa khoảng hợp lệ riêng mà validate đúng
khoảng app đã validate, để không có chỗ nào web chấp nhận một giá trị mà
backend app sẽ từ chối."""

from pydantic import BaseModel, Field


class ProfileOut(BaseModel):
    age: int | None = None
    gender: str | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    fitness_level: str | None = None
    weekly_goal: int | None = None


class ProfileUpdate(BaseModel):
    age: int | None = Field(default=None, ge=1, le=120)
    gender: str | None = Field(default=None, pattern="^(Male|Female|Other)$")
    height_cm: float | None = Field(default=None, ge=140, le=220)
    weight_kg: float | None = Field(default=None, ge=35, le=180)
    fitness_level: str | None = Field(
        default=None, pattern="^(Beginner|Intermediate|Advanced)$"
    )
    weekly_goal: int | None = Field(default=None, ge=1, le=7)


class AccountUpdate(BaseModel):
    """Mirror `UserUpdate` bên backend app — đổi tên hiển thị/mật khẩu."""

    full_name: str | None = None
    password: str | None = Field(default=None, min_length=6)
