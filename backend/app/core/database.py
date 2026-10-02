"""DB riêng của web — CHỈ chứa dữ liệu của riêng web (waitlist, sau này có
thể thêm SupportTickets/Vouchers). KHÔNG có bảng Users — tài khoản thật luôn
nằm bên backend app, xem services/posturex_client.py.

Dùng SQLite (qua aiosqlite) thay vì MySQL: quy mô dữ liệu web (vài nghìn
email waitlist) không cần một DB server riêng, và SQLite không đòi cài đặt
gì ngoài 1 thư viện Python — toàn bộ dữ liệu nằm trong 1 file duy nhất, dễ
backup/di chuyển.
"""

from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_DATA_DIR.mkdir(parents=True, exist_ok=True)
_DB_PATH = _DATA_DIR / "web.db"

engine = create_async_engine(f"sqlite+aiosqlite:///{_DB_PATH}", echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    """Tạo bảng còn thiếu — gọi lúc khởi động app, an toàn chạy lại nhiều lần
    (không xoá bảng/dữ liệu đã có, giống ensure_tables.py bên backend app)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
