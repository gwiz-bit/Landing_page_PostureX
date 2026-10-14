"""Session JWT của web — KHÔNG liên quan gì tới JWT của backend app.

Sau khi backend app xác thực đúng email/mật khẩu, web tự phát hành một JWT
riêng (ký bằng SECRET_KEY của web) để lưu trong cookie HttpOnly của trình
duyệt.

Token JWT gốc (`access_token`) của backend app ĐƯỢC nhúng vào payload này
(xem `backend_access_token`) để các route proxy sau (hồ sơ, danh sách bài
tập...) dùng lại được mà không cần đăng nhập lại — JS phía trình duyệt
không đọc được vì cookie là HttpOnly và payload được ký riêng.
`SESSION_EXPIRE_MINUTES` cố ý khớp `ACCESS_TOKEN_EXPIRE_MINUTES` của backend
app (7 ngày) để hai token luôn hết hạn cùng lúc.
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.core.config import settings

ALGORITHM = "HS256"


def create_session_token(
    user_id: int,
    email: str,
    full_name: str | None,
    phone_number: str | None = None,
    is_admin: bool = False,
    backend_access_token: str | None = None,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "full_name": full_name,
        "phone_number": phone_number,
        "is_admin": is_admin,
        "backend_access_token": backend_access_token,
        "exp": expire,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_session_token(token: str) -> dict | None:
    """Trả về payload nếu hợp lệ, None nếu hết hạn/sai chữ ký — gọi nơi cần
    biết ai đang đăng nhập (vd tạo ticket support), không ném lỗi để chỗ gọi
    tự quyết định (redirect về trang login hay trả 401)."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
