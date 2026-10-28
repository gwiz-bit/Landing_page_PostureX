"""Nâng cấp gói qua Cổng thanh toán SePay (chỉ VietQR) — tạo đơn, hỏi trạng thái, xem gói.

Luồng: `POST /api/upgrade` tạo đơn + trả về form có chữ ký → trình duyệt POST form
sang trang thanh toán của SePay → thanh toán xong SePay gọi IPN (`routes/sepay.py`)
để đơn thành `paid`, rồi đưa người dùng về `payment-result.html`.

Web chỉ bán 1 gói trả phí là Pro (59k/tháng); gói Free không cần mua. GIÁ ở đây là
giá bán trên web — bảng SubscriptionPlans của app chưa đổi theo, xem CLAUDE.md."""

import secrets

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.routes.auth import require_login
from app.core.config import settings
from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.upgrade import STATUS_CANCELLED, STATUS_PENDING, UpgradeRequest
from app.schemas.upgrade import MyPlanOut, OrderStatusOut, UpgradeIn, UpgradeOut
from app.services.upgrade_service import (
    PLAN_PRICES,
    active_expiry,
    build_checkout,
    gateway_configured,
    sync_order_from_gateway,
)

router = APIRouter(prefix="/api/upgrade", tags=["upgrade"])


@router.post("", response_model=UpgradeOut)
@limiter.limit("30/hour")
async def start_order(
    request: Request,
    data: UpgradeIn,
    payload: dict = Depends(require_login),
    db: AsyncSession = Depends(get_db),
) -> UpgradeOut:
    """Bấm "Thanh toán" → tạo MỘT đơn mới và trả về form đã ký để gửi sang SePay."""
    if not gateway_configured():
        raise HTTPException(status_code=503, detail="Cổng thanh toán chưa được cấu hình.")

    user_id = int(payload["sub"])
    plan_name, amount = PLAN_PRICES[data.plan]

    # Mỗi lần bấm = một đơn/mã hoá đơn mới (SePay yêu cầu mã hoá đơn duy nhất). Các đơn
    # chờ cũ của người này đóng lại cho danh sách admin gọn — nhưng IPN vẫn cấp gói nếu
    # khách lỡ trả ở tab cũ (xem routes/sepay.py).
    await db.execute(
        update(UpgradeRequest)
        .where(
            UpgradeRequest.user_id == user_id,
            UpgradeRequest.plan == plan_name,
            UpgradeRequest.status == STATUS_PENDING,
        )
        .values(status=STATUS_CANCELLED)
    )
    order = UpgradeRequest(
        user_id=user_id,
        email=payload["email"],
        full_name=payload.get("full_name"),
        plan=plan_name,
        amount=amount,
        transfer_code="pending",  # điền ngay bên dưới khi đã có id
    )
    db.add(order)
    await db.flush()
    # Hậu tố ngẫu nhiên: mã hoá đơn không bị trùng nếu DB được dựng lại và id đếm lại từ 1.
    order.transfer_code = f"PX{order.id}-{secrets.token_hex(3).upper()}"
    await db.commit()

    base_url = (settings.PUBLIC_BASE_URL or str(request.base_url)).rstrip("/")
    action, fields = build_checkout(order, base_url)
    return UpgradeOut(
        order_id=order.id, invoice=order.transfer_code, amount=order.amount, action=action, fields=fields
    )


@router.get("/order/{order_id}", response_model=OrderStatusOut)
async def order_status(
    order_id: int,
    payload: dict = Depends(require_login),
    db: AsyncSession = Depends(get_db),
) -> OrderStatusOut:
    """Trang kết quả hỏi định kỳ để biết SePay đã báo thanh toán thành công chưa."""
    order = await db.get(UpgradeRequest, order_id)
    # Không phải đơn của mình → coi như không tồn tại (không lộ đơn người khác).
    if order is None or order.user_id != int(payload["sub"]):
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn.")
    # IPN là đường chính, nhưng không phải lúc nào cũng về (Sandbox không phát IPN cho thanh
    # toán giả lập). Chưa thấy "paid" thì hỏi thẳng SePay — chỉ cấp gói khi SePay xác nhận.
    await sync_order_from_gateway(db, order)
    return OrderStatusOut(status=order.status, expires_at=order.expires_at)


@router.get("/me", response_model=MyPlanOut)
async def my_plan(
    payload: dict = Depends(require_login), db: AsyncSession = Depends(get_db)
) -> MyPlanOut:
    expiry = await active_expiry(db, int(payload["sub"]))
    return MyPlanOut(plan="Pro" if expiry else "Free", expires_at=expiry)
