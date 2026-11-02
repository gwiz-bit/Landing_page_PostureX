"""Route chỉ dành cho admin — xem waitlist, góp ý, đơn nâng cấp gói và tài khoản.

Dùng chung tài khoản admin với app PostureX (is_admin nhúng sẵn trong
session JWT của web lúc đăng nhập, xem `routes/auth.py::require_admin`) —
không có bảng Admins riêng của web."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import require_admin
from app.core.database import get_db
from app.models.feedback import Feedback
from app.models.upgrade import STATUS_PAID, STATUS_PENDING, UpgradeRequest, utcnow
from app.services.upgrade_service import grant_paid
from app.models.waitlist import WaitlistSignup
from app.schemas.admin import FeedbackListOut, WaitlistListOut
from app.schemas.admin_users import AdminRoleIn, AdminUserEntry, AdminUserListOut
from app.services.posturex_client import PostureXAuthError, admin_list_users, admin_set_user_admin
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
    """Xử lý tay một đơn đang chờ. Bình thường đơn tự sang "paid" nhờ webhook
    SePay — nút này chỉ để dự phòng khi khách đã chuyển khoản nhưng đơn không
    tự cập nhật (sai nội dung, webhook lỗi...). "paid" cấp gói y như webhook.
    Không kích hoạt gói trong app (app chưa hỗ trợ)."""
    entry = await db.get(UpgradeRequest, upgrade_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn.")
    if entry.status != STATUS_PENDING:
        raise HTTPException(status_code=409, detail="Đơn này đã được xử lý.")
    if data.status == "paid":
        await grant_paid(db, entry, paid_amount=entry.amount)
    else:
        entry.status = data.status
        await db.commit()
    return entry


async def _pro_expiries(db: AsyncSession) -> dict[int, "datetime"]:
    """user_id -> hạn Pro còn hiệu lực (chỉ những người đang còn hạn)."""
    rows = await db.execute(
        select(UpgradeRequest.user_id, func.max(UpgradeRequest.expires_at))
        .where(UpgradeRequest.status == STATUS_PAID)
        .group_by(UpgradeRequest.user_id)
    )
    now = utcnow()
    return {uid: exp for uid, exp in rows if exp and exp > now}


def _user_entry(u: dict, expiries: dict) -> AdminUserEntry:
    exp = expiries.get(u["id"])
    return AdminUserEntry(
        id=u["id"],
        email=u["email"],
        full_name=u.get("full_name"),
        is_admin=u["is_admin"],
        is_active=u["is_active"],
        created_at=u["created_at"],
        plan="Pro" if exp else "Free",
        pro_expires_at=exp,
    )


@router.get("/users", response_model=AdminUserListOut)
async def list_users(
    admin: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)
) -> AdminUserListOut:
    """Tài khoản đã đăng ký (lấy từ backend app) kèm gói Pro (lấy từ DB web)."""
    try:
        users = await admin_list_users(admin["backend_access_token"])
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    expiries = await _pro_expiries(db)
    entries = [_user_entry(u, expiries) for u in users]
    return AdminUserListOut(total=len(entries), entries=entries)


@router.patch("/users/{user_id}/role", response_model=AdminUserEntry)
async def set_user_role(
    user_id: int,
    data: AdminRoleIn,
    admin: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
) -> AdminUserEntry:
    """Cấp/thu quyền admin. Backend app chặn việc tự thu quyền của chính mình (400)."""
    try:
        user = await admin_set_user_admin(admin["backend_access_token"], user_id, data.is_admin)
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return _user_entry(user, await _pro_expiries(db))
