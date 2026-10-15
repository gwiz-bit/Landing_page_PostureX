"""Góp ý của người dùng gửi từ landing page (form "Góp ý của bạn"). Ai cũng gửi
được, không cần tài khoản — chỉ admin xem được (xem routes/admin.py)."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # Không unique — một người có thể gửi nhiều góp ý khác nhau.
    email: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
