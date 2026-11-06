"""Cấu hình slowapi dùng chung — 1 Limiter instance duy nhất, cùng cách làm
với backend app PostureX (xem backend/app/core/rate_limit.py bên đó) để
tránh lặp lại các lỗi đã từng gặp:

- `config_filename=os.devnull`: slowapi tự đọc file `.env` nếu nó tồn tại
  (qua `starlette.config.Config(".env")`), mà `Config` mở file KHÔNG chỉ
  định encoding — trên Windows locale tiếng Việt, comment UTF-8 trong `.env`
  khiến server chết ngay lúc import với `UnicodeDecodeError`. Trỏ sang
  os.devnull để slowapi bỏ qua hẳn việc đọc file (dự án không dùng biến
  RATELIMIT_* nào, cấu hình thật đọc qua app/core/config.py).
- KHÔNG bật `headers_enabled=True`: nhánh thành công của slowapi gọi
  `_inject_headers(kwargs.get("response"), ...)` — endpoint ở đây trả
  Pydantic model, không có tham số `response: Response` nào để nó tìm, nên
  bật cờ đó sẽ làm hỏng MỌI request thành công tới route có rate limit.
"""

import os
import time
import warnings

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from limits import parse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    limiter = Limiter(key_func=get_remote_address, config_filename=os.devnull)


def _format_wait(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds} giây"
    if seconds < 3600:
        return f"{round(seconds / 60)} phút"
    return f"{round(seconds / 3600)} giờ"


def _seconds_until_reset(request: Request) -> int | None:
    current_limit = getattr(request.state, "view_rate_limit", None)
    if current_limit is None:
        return None
    try:
        reset_at, _remaining = limiter.limiter.get_window_stats(current_limit[0], *current_limit[1])
    except Exception:
        return None
    return max(1, int(reset_at - time.time()) + 1)


def _too_many_detail(wait: int | None) -> str:
    if wait is None:
        return "Bạn đã thao tác quá nhiều lần. Vui lòng chờ một lát rồi thử lại."
    return f"Bạn đã thao tác quá nhiều lần. Vui lòng thử lại sau {_format_wait(wait)}."


def ensure_quota(request: Request, limit: str, scope: str) -> None:
    """Hạn mức tự quản lý (bổ sung cho decorator `@limiter.limit`): chỉ KIỂM TRA, không
    trừ lượt. Gọi `consume_quota` sau khi thao tác thành công để trừ.

    slowapi 0.1.10 không có `deduct_when`, mà decorator thì trừ lượt cho MỌI request —
    kể cả lượt bị từ chối (email đã dùng, mật khẩu yếu...). Người dùng thử sai vài lần là
    bị khoá cả giờ dù chưa tạo được tài khoản nào (lỗi "thử lại sau 40 phút" ngày 06/11).
    """
    item = parse(limit)
    key = get_remote_address(request)
    if limiter.limiter.test(item, scope, key):
        return
    try:
        reset_at, _remaining = limiter.limiter.get_window_stats(item, scope, key)
        wait = max(1, int(reset_at - time.time()) + 1)
    except Exception:
        wait = None
    headers = {"Retry-After": str(wait)} if wait is not None else None
    raise HTTPException(status_code=429, detail=_too_many_detail(wait), headers=headers)


def consume_quota(request: Request, limit: str, scope: str) -> None:
    limiter.limiter.hit(parse(limit), scope, get_remote_address(request))


def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Trả 429 với thân `{"detail": ...}` bằng tiếng Việt — khớp đúng khoá
    mà JS phía landing page đọc (`data.detail`, xem các form trong
    landing/*.html), tránh rơi vào thông báo mặc định của slowapi
    (`{"error": ...}`, khoá khác, tiếng Anh)."""
    wait = _seconds_until_reset(request)
    detail = _too_many_detail(wait)
    headers = {"Retry-After": str(wait)} if wait is not None else None
    return JSONResponse(status_code=429, content={"detail": detail}, headers=headers)
