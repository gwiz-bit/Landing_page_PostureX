"""Đăng ký tải trước — chỉ lưu email, không tạo tài khoản PostureX thật."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.waitlist import WaitlistSignup
from app.schemas.waitlist import MessageResponse, WaitlistIn

router = APIRouter(prefix="/api/waitlist", tags=["waitlist"])


@router.post("", response_model=MessageResponse)
@limiter.limit("10/hour")
async def join_waitlist(
    request: Request, data: WaitlistIn, db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    existing = await db.scalar(select(WaitlistSignup).where(WaitlistSignup.email == data.email))
    if existing is not None:
        # Không coi là lỗi — người dùng bấm lại/đăng ký lại cùng email vẫn
        # nên thấy thông báo thành công, không phải lý do chặn trải nghiệm.
        return MessageResponse(message="Email này đã có trong danh sách chờ rồi!")

    db.add(WaitlistSignup(email=data.email, source=data.source))
    await db.commit()
    return MessageResponse(message="Cảm ơn bạn! Chúng tôi sẽ báo ngay khi PostureX ra mắt.")
