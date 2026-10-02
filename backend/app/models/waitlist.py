"""Danh sách email đăng ký nhận thông báo khi app ra mắt ("đăng ký tải
trước"). Đây KHÔNG phải tài khoản PostureX — không mật khẩu, không liên hệ
backend app, chỉ là lead marketing thuần (xem CTA "Sắp ra mắt" ở landing
page)."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class WaitlistSignup(Base):
    __tablename__ = "waitlist_signups"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    # Vị trí trên trang người dùng bấm đăng ký (vd "hero", "download") — giúp
    # biết CTA nào hiệu quả hơn, không bắt buộc phải điền đúng.
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
