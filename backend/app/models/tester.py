"""Email người dùng đăng ký làm tester (chương trình thử nghiệm kín trên Google
Play). Leader xem danh sách ở trang admin rồi thêm TAY vào Play Console — web
không tự thêm được và không kiểm tra được ai đã thực sự tham gia."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TesterSignup(Base):
    __tablename__ = "tester_signups"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
