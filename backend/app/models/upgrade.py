"""Yêu cầu nâng cấp gói (Premium/Pro) bằng chuyển khoản thủ công.

Web KHÔNG xác nhận được tiền đã về và KHÔNG kích hoạt gói trong app (backend
app đang tắt bán hàng, nhóm chưa cho sửa). Bảng này chỉ ghi lại "người dùng X
báo đã chuyển khoản gói Y" để leader đối chiếu sao kê rồi tự kích hoạt gói
trong app, sau đó đánh dấu trạng thái ở trang admin."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

STATUS_PENDING = "pending"
STATUS_APPROVED = "approved"  # leader đã kích hoạt gói cho người dùng
STATUS_REJECTED = "rejected"


class UpgradeRequest(Base):
    __tablename__ = "upgrade_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    # id/email lấy từ session đăng nhập (backend app), không phải do client gửi.
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    plan: Mapped[str] = mapped_column(String(20), nullable=False)
    # Giá tại thời điểm tạo đơn, tính ở server (không tin số tiền client gửi).
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    # Nội dung chuyển khoản, vd "PX12-PRO" — để đối chiếu sao kê.
    transfer_code: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_PENDING, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
