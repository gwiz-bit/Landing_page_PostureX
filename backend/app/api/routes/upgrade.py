"""Nâng cấp gói bằng chuyển khoản — người dùng báo "đã chuyển khoản".

Tên gói khớp bảng SubscriptionPlans của app (Premium, Pro) nhưng GIÁ ở đây
(59k/89k) là giá bán trên web — app chưa đổi theo, xem CLAUDE.md."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import require_login
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.upgrade import STATUS_PENDING, UpgradeRequest
from app.schemas.upgrade import UpgradeIn, UpgradeOut

router = APIRouter(prefix="/api/upgrade", tags=["upgrade"])

# Giá/tháng (VND) theo mã gói client gửi. Nguồn duy nhất ở server.
PLAN_PRICES = {"premium": ("Premium", 59000), "pro": ("Pro", 89000)}


def transfer_code(user_id: int, plan_key: str) -> str:
    return f"PX{user_id}-{plan_key.upper()}"


@router.post("", response_model=UpgradeOut)
@limiter.limit("10/hour")
async def request_upgrade(
    request: Request,
    data: UpgradeIn,
    payload: dict = Depends(require_login),
    db: AsyncSession = Depends(get_db),
) -> UpgradeOut:
    user_id = int(payload["sub"])
    plan_name, amount = PLAN_PRICES[data.plan]
    code = transfer_code(user_id, data.plan)

    # Bấm "Tôi đã chuyển khoản" nhiều lần không tạo thêm đơn — dùng lại đơn
    # đang chờ của đúng người + đúng gói.
    existing = await db.scalar(
        select(UpgradeRequest).where(
            UpgradeRequest.user_id == user_id,
            UpgradeRequest.plan == plan_name,
            UpgradeRequest.status == STATUS_PENDING,
        )
    )
    if existing is None:
        db.add(
            UpgradeRequest(
                user_id=user_id,
                email=payload["email"],
                full_name=payload.get("full_name"),
                plan=plan_name,
                amount=amount,
                transfer_code=code,
            )
        )
        await db.commit()
    return UpgradeOut(message="Đã ghi nhận yêu cầu nâng cấp.", transfer_code=code, amount=amount)
