"""Route chỉ dành cho admin — xem waitlist, góp ý và đơn nâng cấp gói.

Dùng chung tài khoản admin với app PostureX (is_admin nhúng sẵn trong
session JWT của web lúc đăng nhập, xem `routes/auth.py::require_admin`) —
không có bảng Admins riêng của web."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import require_admin
from app.core.database import get_db
from app.models.feedback import Feedback
from app.models.upgrade import STATUS_PENDING, UpgradeRequest
from app.models.waitlist import WaitlistSignup
from app.schemas.admin import FeedbackListOut, WaitlistListOut
from app.schemas.upgrade import UpgradeEntryOut, UpgradeListOut, UpgradeStatusIn

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


@router.get("/feedback", response_model=FeedbackListOut)
async def list_feedback(
    _admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)
) -> FeedbackListOut:
    result = await db.scalars(select(Feedback).order_by(Feedback.created_at.desc()))
    entries = list(result)
    return FeedbackListOut(total=len(entries), entries=entries)


@router.get("/upgrades", response_model=UpgradeListOut)
async def list_upgrades(
    _admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)
) -> UpgradeListOut:
    result = await db.scalars(select(UpgradeRequest).order_by(UpgradeRequest.created_at.desc()))
    entries = list(result)
    return UpgradeListOut(total=len(entries), entries=entries)


@router.patch("/upgrades/{upgrade_id}", response_model=UpgradeEntryOut)
async def set_upgrade_status(
    upgrade_id: int,
    data: UpgradeStatusIn,
    _admin: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> UpgradeEntryOut:
    """Đánh dấu đơn đã xử lý. KHÔNG kích hoạt gói trong app — leader tự làm
    việc đó trong app trước, rồi mới bấm "approved" ở đây để ghi nhận."""
    entry = await db.get(UpgradeRequest, upgrade_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn.")
    if entry.status != STATUS_PENDING:
        raise HTTPException(status_code=409, detail="Đơn này đã được xử lý.")
    entry.status = data.status
    await db.commit()
    return entry
