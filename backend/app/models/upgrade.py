"""Đơn nâng cấp gói (Pro) trả bằng chuyển khoản, tự xác nhận qua SePay.

Luồng: người dùng mở trang thanh toán → web tạo 1 đơn `pending` (mã chuyển
khoản `PX<user_id>PRO`) → người dùng quét QR chuyển khoản → SePay báo về
webhook → đơn chuyển sang `paid` và gói Pro có hạn `expires_at`.

⚠️ "Gói của người dùng" chỉ tồn tại phía WEB (đọc từ bảng này). Backend app
đang tắt bán hàng và nhóm chưa cho sửa, nên gói Pro CHƯA mở khoá gì trong app —
chỉ web ghi nhận ai đã trả tiền, hạn tới khi nào, để admin xem."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

STATUS_PENDING = "pending"      # đã tạo đơn, chưa thấy tiền
STATUS_PAID = "paid"            # đã nhận tiền, gói đang/đã có hạn
STATUS_CANCELLED = "cancelled"  # admin huỷ


def utcnow() -> datetime:
    """Giờ UTC dạng naive — SQLite không lưu timezone, cả bảng dùng cùng quy ước."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class UpgradeRequest(Base):
    __tablename__ = "upgrade_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    # id/email lấy từ session đăng nhập (backend app), không phải do client gửi.
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    # Rỗng nếu đơn được tạo từ webhook mà web chưa từng thấy người dùng này.
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    plan: Mapped[str] = mapped_column(String(20), nullable=False)
    # Giá tại thời điểm tạo đơn, tính ở server (không tin số tiền client gửi).
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    # Nội dung chuyển khoản, vd "PX12PRO" — SePay đối chiếu theo mã này.
    transfer_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_PENDING, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # --- điền khi đã thanh toán (cột thêm sau, xem core/database.py::init_db) ---
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    paid_amount: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # id giao dịch phía SePay — chống xử lý lặp khi SePay gọi lại webhook.
    # Duy nhất qua unique index tạo trong init_db (ALTER TABLE không thêm được UNIQUE).
    sepay_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
