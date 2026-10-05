"""Route chỉ dành cho admin — hiện tại chỉ có xem danh sách waitlist.

Dùng chung tài khoản admin với app PostureX (is_admin nhúng sẵn trong
session JWT của web lúc đăng nhập, xem `routes/auth.py::require_admin`) —
không có bảng Admins riêng của web."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import require_admin
from app.core.database import get_db
from app.models.waitlist import WaitlistSignup
from app.schemas.admin import WaitlistListOut

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/waitlist", response_model=WaitlistListOut)
async def list_waitlist(
    _admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)
) -> WaitlistListOut:
    result = await db.scalars(
        select(WaitlistSignup).order_by(WaitlistSignup.created_at.desc())
    )
    entries = list(result)
    return WaitlistListOut(total=len(entries), entries=entries)
