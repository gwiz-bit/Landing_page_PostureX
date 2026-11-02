from datetime import datetime

from pydantic import BaseModel


class AdminUserEntry(BaseModel):
    id: int
    email: str
    full_name: str | None
    is_admin: bool
    is_active: bool
    created_at: datetime
    # "Pro" nếu đang còn hạn (đọc từ DB web), ngược lại "Free".
    plan: str
    pro_expires_at: datetime | None


class AdminUserListOut(BaseModel):
    total: int
    entries: list[AdminUserEntry]


class AdminRoleIn(BaseModel):
    is_admin: bool
