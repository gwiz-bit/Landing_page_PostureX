"""Backend web PostureX — phục vụ landing page tĩnh + API login/support/voucher.

Đây là repo RIÊNG, tách hẳn khỏi backend app PostureX (MoMo/Google Play/pose
analysis...) — chỉ gọi sang backend app qua HTTP để xác thực tài khoản (xem
services/posturex_client.py), không dùng chung DB.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth, waitlist
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router)
app.include_router(waitlist.router)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "app": settings.APP_NAME}


# Mount PHẢI đứng SAU mọi route khác — Starlette khớp theo đúng thứ tự đăng
# ký, và Mount("/") khớp MỌI đường dẫn. Đặt trước sẽ nuốt mất /health và
# /api/auth/* trước khi chúng kịp được xét tới.
_LANDING_DIR = Path(__file__).resolve().parent.parent.parent / "landing"
if _LANDING_DIR.exists():
    app.mount("/", StaticFiles(directory=_LANDING_DIR, html=True), name="landing")
