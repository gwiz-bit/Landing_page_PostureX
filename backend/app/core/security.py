"""Session JWT của web — KHÔNG liên quan gì tới JWT của backend app.

Sau khi backend app xác thực đúng email/mật khẩu, web tự phát hành một JWT
riêng (ký bằng SECRET_KEY của web) để lưu trong cookie HttpOnly của trình
duyệt. Token JWT gốc từ backend app không được lưu lại lâu dài — chỉ dùng
đúng 1 lần lúc đăng nhập để gọi /users/me lấy thông tin hiển thị.
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
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.SESSION_EXPIRE_MINUTES)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "full_name": full_name,
        "phone_number": phone_number,
        "is_admin": is_admin,
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
