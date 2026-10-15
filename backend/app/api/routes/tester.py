"""Đăng ký làm tester — công khai, chỉ lưu email."""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.rate_limit import limiter
from app.models.tester import TesterSignup
from app.schemas.tester import TesterIn
from app.schemas.waitlist import MessageResponse

router = APIRouter(prefix="/api/tester", tags=["tester"])

# Email trường học thường là tài khoản Google Workspace bị quản trị viên chặn,
# nên không cài được app thử nghiệm. Chỉ chặn được đuôi trường học — email
# doanh nghiệp không có dấu hiệu nhận diện, đã dặn người dùng ngay trên form.
_BLOCKED_DOMAIN_SUFFIXES = (".edu", ".edu.vn", ".ac.vn")


@router.post("", response_model=MessageResponse)
@limiter.limit("10/hour")
async def join_testers(
    request: Request, data: TesterIn, db: AsyncSession = Depends(get_db)
) -> MessageResponse:
    email = data.email.strip().lower()
    domain = email.rsplit("@", 1)[-1]
    if domain.endswith(_BLOCKED_DOMAIN_SUFFIXES):
        raise HTTPException(
            status_code=400,
            detail="Không dùng email sinh viên/trường học. Vui lòng dùng email trùng với tài khoản CH Play của bạn.",
        )

    existing = await db.scalar(select(TesterSignup).where(TesterSignup.email == email))
    if existing is None:
        db.add(TesterSignup(email=email))
        await db.commit()
    # Đã đăng ký rồi vẫn coi là thành công để người dùng đi tiếp sang bước 2.
    return MessageResponse(message="Đã nhận email của bạn.")
