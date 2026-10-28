"""Các đường SePay gọi vào web.

1) `POST /api/sepay/ipn` — IPN của CỔNG THANH TOÁN (cách đang dùng): SePay báo đơn đã thanh
   toán thành công. Cấu hình IPN bên SePay: URL `https://<domain>/api/sepay/ipn`, kiểu xác
   thực SECRET_KEY (SePay gửi header `X-Secret-Key` = SECRET KEY của merchant).

2) `POST /api/sepay/webhook` — webhook THEO DÕI SỐ DƯ tài khoản ngân hàng (cách cũ, trang
   thanh toán hiện không còn dùng; giữ lại để khỏi mất code, không cấu hình thì vô hại).

Webhook theo dõi số dư — SePay gọi vào đây mỗi khi tài khoản ngân hàng có biến động số dư.

Cần địa chỉ HTTPS công khai (localhost thì SePay không gọi tới được). Cấu hình
bên SePay: URL `https://<domain>/api/sepay/webhook`, kiểu xác thực "API Key",
giá trị khớp `SEPAY_API_KEY` trong `.env`.

Định dạng payload/header ở đây theo tài liệu SePay tại thời điểm viết — nhóm nên
đối chiếu lại với trang cấu hình webhook của SePay khi kết nối thật."""

import hmac
import logging
from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.upgrade import STATUS_PAID, STATUS_PENDING, UpgradeRequest
from app.services.upgrade_service import CODE_RE, PLAN_PRICES, grant_paid, transfer_code

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/sepay", tags=["sepay"])

_OK = {"success": True}


@router.post("/webhook")
async def sepay_webhook(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    # Chưa cấu hình khoá thì KHÔNG nhận gì — nếu không ai cũng giả được "đã chuyển tiền".
    if not settings.SEPAY_API_KEY:
        raise HTTPException(status_code=503, detail="Chưa cấu hình SEPAY_API_KEY.")
    expected = f"Apikey {settings.SEPAY_API_KEY}"
    if not hmac.compare_digest(request.headers.get("Authorization", "").encode(), expected.encode()):
        raise HTTPException(status_code=401, detail="Sai khoá xác thực.")

    payload = await request.json()

    # Chỉ quan tâm tiền VÀO, và đúng tài khoản nhận (nếu có cấu hình số tài khoản).
    if payload.get("transferType") != "in":
        return _OK
    if settings.SEPAY_ACCOUNT_NUMBER and payload.get("accountNumber") != settings.SEPAY_ACCOUNT_NUMBER:
        return _OK

    sepay_id = payload.get("id")
    try:
        amount = int(payload.get("transferAmount", 0))
    except (TypeError, ValueError):
        return _OK

    # Mã thanh toán nằm ở `code` (nếu SePay nhận diện được) hoặc trong `content`.
    text = f"{payload.get('code') or ''} {payload.get('content') or ''}"
    match = CODE_RE.search(text)
    if match is None:
        return _OK  # khoản tiền không liên quan tới gói nào của web
    user_id = int(match.group(1))
    plan_name, price = PLAN_PRICES["pro"]

    # Chống xử lý lặp: SePay có thể gọi lại cùng một giao dịch.
    if sepay_id is not None:
        done = await db.scalar(select(UpgradeRequest).where(UpgradeRequest.sepay_id == sepay_id))
        if done is not None:
            return _OK

    # Người dùng có thể sửa số tiền trong app ngân hàng → phải đủ tiền mới cấp gói.
    # Thiếu tiền: không cấp, đơn vẫn pending để admin xử lý tay (log để đối soát).
    if amount < price:
        logger.warning("SePay #%s: %sđ < %sđ cho mã %s — không cấp gói", sepay_id, amount, price, match.group(0))
        return _OK

    order = await db.scalar(
        select(UpgradeRequest)
        .where(
            UpgradeRequest.user_id == user_id,
            UpgradeRequest.plan == plan_name,
            UpgradeRequest.status == STATUS_PENDING,
        )
        .order_by(UpgradeRequest.id.desc())
    )
    if order is None:
        # Có tiền về mà web chưa có đơn (vd người dùng dùng lại QR cũ): vẫn ghi
        # nhận để không mất tiền của khách; email chưa biết nên để rỗng.
        order = UpgradeRequest(
            user_id=user_id,
            email="",
            full_name=None,
            plan=plan_name,
            amount=price,
            transfer_code=transfer_code(user_id, "pro"),
        )
        db.add(order)
        await db.flush()

    await grant_paid(db, order, paid_amount=amount, sepay_id=sepay_id)
    logger.info("SePay #%s: user %s đã thanh toán %sđ — gói %s tới %s", sepay_id, user_id, amount, plan_name, order.expires_at)
    return _OK


@router.post("/ipn")
async def sepay_ipn(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    """IPN của Cổng thanh toán: `notification_type=ORDER_PAID` nghĩa là khách đã trả xong."""
    secret = settings.SEPAY_PG_SECRET_KEY
    # Chưa cấu hình khoá thì KHÔNG nhận gì — nếu không ai cũng giả được "đã thanh toán".
    if not secret:
        raise HTTPException(status_code=503, detail="Chưa cấu hình SEPAY_PG_SECRET_KEY.")
    if not hmac.compare_digest(request.headers.get("X-Secret-Key", "").encode(), secret.encode()):
        raise HTTPException(status_code=401, detail="Sai khoá xác thực.")

    payload = await request.json()
    # Chỉ xử lý thanh toán thành công; TRANSACTION_VOID (huỷ giao dịch) bỏ qua — leader xử lý tay.
    if payload.get("notification_type") != "ORDER_PAID":
        return _OK

    info = payload.get("order") or {}
    invoice = info.get("order_invoice_number")
    if not invoice:
        return _OK

    # Tìm đơn theo mã hoá đơn, mọi trạng thái trừ đã trả: khách trả ở tab cũ (đơn đã bị đóng
    # khi họ bấm thanh toán lại) hoặc admin lỡ huỷ thì vẫn phải cấp gói, không giữ tiền của khách.
    order = await db.scalar(select(UpgradeRequest).where(UpgradeRequest.transfer_code == invoice))
    if order is None:
        logger.warning("SePay IPN: không có đơn nào mang mã hoá đơn %s", invoice)
        return _OK
    if order.status == STATUS_PAID:  # IPN có thể bị gửi lặp
        return _OK

    try:
        paid = Decimal(str(info.get("order_amount", "0")))
    except InvalidOperation:
        return _OK
    # Số tiền do SePay báo, vẫn so lại với giá của đơn (do server đặt lúc tạo đơn).
    if paid < order.amount:
        logger.warning("SePay IPN %s: nhận %s < %s — không cấp gói", invoice, paid, order.amount)
        return _OK

    await grant_paid(db, order, paid_amount=int(paid))
    logger.info("SePay IPN %s: user %s đã thanh toán %s — gói %s tới %s", invoice, order.user_id, paid, order.plan, order.expires_at)
    return _OK
