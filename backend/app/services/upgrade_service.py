"""Logic dùng chung cho đơn nâng cấp: giá, mã chuyển khoản, và cấp gói khi đã thu tiền."""

import base64
import hashlib
import hmac
import logging
import re
from datetime import timedelta
from decimal import Decimal, InvalidOperation

import httpx

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.upgrade import STATUS_PAID, UpgradeRequest, utcnow

# Giá/tháng (VND) theo mã gói. Nguồn duy nhất ở server.
PLAN_PRICES = {"pro": ("Pro", 59000)}
PLAN_DAYS = 30
# Còn bao nhiêu ngày thì được mua tiếp. 0 = khoá việc mua cho tới khi gói HẾT HẠN hẳn
# (không gia hạn sớm). Muốn cho gia hạn sớm vài ngày cuối thì tăng số này (vd 3).
RENEW_BEFORE_DAYS = 0

# Mã chỉ gồm chữ + số (không dấu gạch): ngân hàng/SePay hay cắt hoặc đổi ký tự lạ
# trong nội dung chuyển khoản. Khớp không phân biệt hoa/thường vì app ngân hàng
# có thể tự viết hoa/thường lại nội dung.
CODE_RE = re.compile(r"PX(\d+)PRO", re.IGNORECASE)


def transfer_code(user_id: int, plan_key: str) -> str:
    return f"PX{user_id}{plan_key.upper()}"


async def grant_paid(
    db: AsyncSession, order: UpgradeRequest, paid_amount: int, sepay_id: int | None = None
) -> UpgradeRequest:
    """Đánh dấu đơn đã thanh toán và tính hạn gói.

    Gia hạn cộng dồn: nếu người dùng còn gói Pro chưa hết hạn thì hạn mới tính
    từ hạn cũ, không từ hôm nay (không ăn mất ngày họ đã trả)."""
    now = utcnow()
    latest_expiry = await db.scalar(
        select(func.max(UpgradeRequest.expires_at)).where(
            UpgradeRequest.user_id == order.user_id,
            UpgradeRequest.status == STATUS_PAID,
        )
    )
    start = latest_expiry if latest_expiry and latest_expiry > now else now
    order.status = STATUS_PAID
    order.paid_at = now
    order.expires_at = start + timedelta(days=PLAN_DAYS)
    order.paid_amount = paid_amount
    if sepay_id is not None:
        order.sepay_id = sepay_id
    await db.commit()
    return order


async def active_expiry(db: AsyncSession, user_id: int):
    """Hạn gói Pro còn hiệu lực của người dùng, hoặc None nếu đang dùng Free."""
    expiry = await db.scalar(
        select(func.max(UpgradeRequest.expires_at)).where(
            UpgradeRequest.user_id == user_id,
            UpgradeRequest.status == STATUS_PAID,
        )
    )
    return expiry if expiry and expiry > utcnow() else None


# ---------------------------------------------------------------------------
# Cổng thanh toán SePay (VietQR). Không có SDK Python nên tự ký theo mã nguồn SDK Node
# của SePay (sepay-pg-node, src/checkout.ts): ghép "tên=giá_trị" theo ĐÚNG thứ tự trường
# gửi đi, nối bằng dấu phẩy, HMAC-SHA256 bằng SECRET KEY, xuất base64.
# ---------------------------------------------------------------------------

CHECKOUT_INIT_URL = {
    "sandbox": "https://pay-sandbox.sepay.vn/v1/checkout/init",
    "production": "https://pay.sepay.vn/v1/checkout/init",
}


def gateway_configured() -> bool:
    return bool(settings.SEPAY_PG_MERCHANT_ID and settings.SEPAY_PG_SECRET_KEY)


def sign_fields(fields: dict[str, str], secret_key: str) -> str:
    """Chữ ký của form checkout. Thứ tự trong `fields` chính là thứ tự được ký."""
    payload = ",".join(f"{k}={v}" for k, v in fields.items())
    digest = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def build_checkout(order: UpgradeRequest, base_url: str) -> tuple[str, dict[str, str]]:
    """URL + các trường của form gửi sang SePay cho một đơn (chỉ phương thức VietQR).

    Thứ tự trường theo bảng tham số trong tài liệu SePay, `merchant` ở cuối (SDK Node
    cũng thêm `merchant` vào cuối khi người gọi không tự đưa vào). Số tiền gửi dạng
    chuỗi số nguyên và PHẢI khớp giá trị đã ký. Nếu SePay báo sai chữ ký khi test trên
    Sandbox thì thứ tự này là chỗ đầu tiên cần xem lại."""
    result_url = f"{base_url}/payment-result.html?order={order.id}"
    fields = {
        "operation": "PURCHASE",
        "payment_method": "BANK_TRANSFER",
        "order_invoice_number": order.transfer_code,
        "order_amount": str(order.amount),
        "currency": "VND",
        "order_description": f"Nang cap goi {order.plan} PostureX",
        "success_url": f"{result_url}&status=success",
        "error_url": f"{result_url}&status=error",
        "cancel_url": f"{result_url}&status=cancel",
        "merchant": settings.SEPAY_PG_MERCHANT_ID,
    }
    fields["signature"] = sign_fields(fields, settings.SEPAY_PG_SECRET_KEY)
    env = settings.SEPAY_PG_ENV if settings.SEPAY_PG_ENV in CHECKOUT_INIT_URL else "sandbox"
    return CHECKOUT_INIT_URL[env], fields


# ---------------------------------------------------------------------------
# Hỏi lại API của SePay xem một đơn đã thanh toán chưa — đường dự phòng khi IPN không
# về (Sandbox không phát IPN cho thanh toán giả lập; production thì IPN có thể lỗi/chậm).
# Là cuộc gọi server → SePay có xác thực (Basic = MERCHANT ID:SECRET KEY) nên đáng tin
# hơn mọi thứ trên URL trình duyệt.
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)

PG_API_URL = {
    "sandbox": "https://pgapi-sandbox.sepay.vn/v1",
    "production": "https://pgapi.sepay.vn/v1",
}


async def fetch_gateway_order(invoice: str) -> dict | None:
    """Chi tiết đơn bên SePay theo mã hoá đơn, hoặc None nếu không hỏi được."""
    env = settings.SEPAY_PG_ENV if settings.SEPAY_PG_ENV in PG_API_URL else "sandbox"
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(
                f"{PG_API_URL[env]}/order/detail/{invoice}",
                auth=(settings.SEPAY_PG_MERCHANT_ID, settings.SEPAY_PG_SECRET_KEY),
            )
        if resp.status_code != 200:
            return None
        return (resp.json() or {}).get("data")
    except (httpx.HTTPError, ValueError):
        logger.warning("Không hỏi được SePay về đơn %s", invoice)
        return None


async def sync_order_from_gateway(db: AsyncSession, order: UpgradeRequest) -> bool:
    """Nếu SePay báo đơn đã thanh toán (CAPTURED) đủ tiền thì cấp gói. Trả True nếu vừa cấp."""
    if order.status == STATUS_PAID or not gateway_configured():
        return False
    info = await fetch_gateway_order(order.transfer_code)
    if not info or info.get("order_invoice_number") != order.transfer_code:
        return False
    if info.get("order_status") != "CAPTURED":
        return False
    try:
        paid = Decimal(str(info.get("order_amount", "0")))
    except InvalidOperation:
        return False
    # Số tiền SePay báo vẫn phải đủ so với giá đơn (do server đặt lúc tạo đơn).
    if paid < order.amount:
        logger.warning("SePay đơn %s: %s < %s — không cấp gói", order.transfer_code, paid, order.amount)
        return False
    await grant_paid(db, order, paid_amount=int(paid))
    logger.info("Đơn %s: SePay báo đã thanh toán — cấp gói cho user %s tới %s", order.transfer_code, order.user_id, order.expires_at)
    return True


def can_renew(expiry) -> bool:
    """Người đang có gói còn hạn `expiry` (hoặc None = đang Free) có được mua tiếp không."""
    return expiry is None or (expiry - utcnow()) <= timedelta(days=RENEW_BEFORE_DAYS)
