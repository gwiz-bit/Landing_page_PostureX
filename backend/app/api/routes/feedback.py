"""Nhận góp ý từ landing page — công khai, không cần đăng nhập."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackIn
from app.schemas.waitlist import MessageResponse

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=MessageResponse)
@limiter.limit("5/hour")
async def submit_feedback(
    request: Request, data: FeedbackIn, db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    # Honeypot bị điền → bot. Vẫn trả thành công để bot không biết bị chặn,
    # nhưng KHÔNG lưu gì.
    if not data.website:
        db.add(Feedback(name=data.name, email=data.email, message=data.message))
        await db.commit()
    return MessageResponse(message="Cảm ơn bạn đã gửi góp ý!")
