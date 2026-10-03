"""Backend web PostureX — phục vụ landing page tĩnh + API login/support/voucher.

Đây là repo RIÊNG, tách hẳn khỏi backend app PostureX (MoMo/Google Play/pose
analysis...) — chỉ gọi sang backend app qua HTTP để xác thực tài khoản (xem
services/posturex_client.py), không dùng chung DB.
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import auth, waitlist
from app.core.config import settings
from app.core.database import init_db
from app.core.rate_limit import limiter, rate_limit_handler

app = FastAPI(title=settings.APP_NAME)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.include_router(auth.router)
app.include_router(waitlist.router)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": settings.APP_NAME}


_LANDING_DIR = Path(__file__).resolve().parent.parent.parent / "landing"


@app.exception_handler(StarletteHTTPException)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    """Trang 404 có giao diện thay vì {"detail": "Not Found"} trần trụi —
    chỉ áp dụng cho request KHÔNG phải gọi API (đường dẫn không bắt đầu
    bằng /api), để lỗi 404 của API vẫn trả JSON như bình thường cho code
    gọi nó (vd fetch() trong landing page kiểm tra response.ok).

    Bắt `starlette.exceptions.HTTPException` (lớp GỐC), không phải
    `fastapi.exceptions.HTTPException` (chỉ là lớp con) — StaticFiles của
    Starlette (phục vụ landing page tĩnh) ném thẳng lớp gốc khi không tìm
    thấy file, bắt nhầm lớp con sẽ không khớp được exception đó."""
    if exc.status_code == 404 and not request.url.path.startswith("/api"):
        # Tên file CỐ TÌNH không phải "404.html" — StaticFiles(html=True) của
        # Starlette tự nhận diện đúng tên đó và trả file ngay bên trong chính
        # nó (staticfiles.py, trước khi kịp raise HTTPException), bỏ qua
        # hoàn toàn handler này — kể cả cho path /api/* sai. Đổi tên để chỉ
        # có handler này (biết phân biệt /api/* và trang thường) mới serve nó.
        not_found_file = _LANDING_DIR / "not-found.html"
        if not_found_file.exists():
            return FileResponse(not_found_file, status_code=404)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# Mount PHẢI đứng SAU mọi route khác — Starlette khớp theo đúng thứ tự đăng
# ký, và Mount("/") khớp MỌI đường dẫn. Đặt trước sẽ nuốt mất /health và
# /api/auth/* trước khi chúng kịp được xét tới.
if _LANDING_DIR.exists():
    app.mount("/", StaticFiles(directory=_LANDING_DIR, html=True), name="landing")
