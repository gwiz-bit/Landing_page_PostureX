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

from fastapi import Request
from fastapi.responses import JSONResponse
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


def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Trả 429 với thân `{"detail": ...}` bằng tiếng Việt — khớp đúng khoá
    mà JS phía landing page đọc (`data.detail`, xem các form trong
    landing/*.html), tránh rơi vào thông báo mặc định của slowapi
    (`{"error": ...}`, khoá khác, tiếng Anh)."""
    wait = _seconds_until_reset(request)
    if wait is None:
        detail = "Bạn đã thao tác quá nhiều lần. Vui lòng chờ một lát rồi thử lại."
    else:
        detail = f"Bạn đã thao tác quá nhiều lần. Vui lòng thử lại sau {_format_wait(wait)}."

    headers = {"Retry-After": str(wait)} if wait is not None else None
    return JSONResponse(status_code=429, content={"detail": detail}, headers=headers)
