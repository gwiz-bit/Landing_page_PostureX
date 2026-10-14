"""Gọi sang backend app PostureX (repo khác) để xác thực người dùng.

Web KHÔNG có bảng Users riêng — mỗi lần đăng nhập, backend web gọi thẳng
API đã có sẵn của backend app (server-to-server qua httpx, không phải
browser gọi trực tiếp, nên không đụng tới CORS của backend app). Nguồn sự
thật duy nhất về tài khoản luôn là backend app.
"""

import httpx

from app.core.config import settings


class PostureXAuthError(Exception):
    """Đăng nhập thất bại — message lấy từ chính `detail` backend app trả về,
    hiển thị lại cho user y hệt như app mobile đang làm."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


async def register(email: str, password: str, full_name: str | None) -> dict:
    """Tạo tài khoản mới bên backend app — tài khoản này dùng chung được trên
    cả app lẫn web vì cùng một backend/DB thật. Trả về user chưa xác thực
    (is_email_verified=False); backend app tự gửi OTP tới email, web chỉ cần
    hứng kết quả và dẫn người dùng sang bước nhập OTP."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.post(
            "/auth/register",
            json={"email": email, "password": password, "full_name": full_name},
        )
        if resp.status_code != 201:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json()


async def verify_otp_and_fetch_profile(email: str, otp_code: str) -> tuple[dict, str]:
    """Xác thực OTP vừa đăng ký — /auth/verify-otp trả access_token luôn
    (kiêm đăng nhập lần đầu), rồi gọi tiếp /users/me như login thường.

    Trả về (profile, access_token) — access_token nhúng vào session cookie
    của web để các route proxy sau (hồ sơ, bài tập...) dùng lại được, xem
    `core/security.py::create_session_token`."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        verify_resp = await client.post(
            "/auth/verify-otp", json={"email": email, "otp_code": otp_code}
        )
        if verify_resp.status_code != 200:
            raise PostureXAuthError(verify_resp.status_code, _extract_detail(verify_resp))

        access_token = verify_resp.json()["access_token"]
        me_resp = await client.get(
            "/users/me", headers={"Authorization": f"Bearer {access_token}"}
        )
        if me_resp.status_code != 200:
            raise PostureXAuthError(502, "Xác thực thành công nhưng không lấy được hồ sơ.")
        return me_resp.json(), access_token


async def resend_otp(email: str) -> str:
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.post("/auth/resend-otp", json={"email": email})
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json().get("message", "Đã gửi lại mã OTP.")


async def login_and_fetch_profile(email: str, password: str) -> tuple[dict, str]:
    """Đăng nhập bằng /auth/login rồi lấy thông tin qua /users/me.

    Hai lời gọi tuần tự vì /auth/login chỉ trả về access_token, không kèm
    tên/email/sđt (xem backend/app/schemas/auth.py::TokenResponse của repo
    app) — đúng thiết kế hiện tại của backend app, không phải thiếu sót.

    Trả về (profile, access_token) — xem docstring của
    `verify_otp_and_fetch_profile` cho lý do access_token được trả ra.
    """
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        login_resp = await client.post(
            "/auth/login", json={"email": email, "password": password}
        )
        if login_resp.status_code != 200:
            detail = _extract_detail(login_resp)
            raise PostureXAuthError(login_resp.status_code, detail)

        access_token = login_resp.json()["access_token"]

        me_resp = await client.get(
            "/users/me", headers={"Authorization": f"Bearer {access_token}"}
        )
        if me_resp.status_code != 200:
            # Không nên xảy ra nếu /auth/login vừa thành công, nhưng vẫn xử lý
            # rõ ràng thay vì để KeyError mơ hồ nếu backend app đổi hành vi.
            raise PostureXAuthError(502, "Đăng nhập thành công nhưng không lấy được hồ sơ.")

        return me_resp.json(), access_token


async def get_profile(access_token: str) -> dict:
    """Proxy GET /users/me/profile — hồ sơ thể chất (tuổi/chiều cao/cân
    nặng/giới tính/trình độ/mục tiêu tuần) dùng cho trang Hồ sơ và Home."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.get(
            "/users/me/profile", headers={"Authorization": f"Bearer {access_token}"}
        )
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json()


async def update_profile(access_token: str, data: dict) -> dict:
    """Proxy PUT /users/me/profile — lưu hồ sơ thể chất."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.put(
            "/users/me/profile",
            json=data,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json()


async def update_account(access_token: str, data: dict) -> dict:
    """Proxy PATCH /users/me — đổi tên hiển thị/mật khẩu."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.patch(
            "/users/me",
            json=data,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json()


async def list_exercises() -> list[dict]:
    """Proxy GET /exercises — endpoint công khai phía backend app (không cần
    token), nhưng vẫn đi qua web để trình duyệt không cần gọi thẳng sang
    domain backend app (tránh phải mở CORS riêng cho domain web)."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.get("/exercises")
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, "Không tải được danh sách bài tập.")
        return resp.json()


async def request_password_reset(email: str) -> str:
    """Proxy POST /auth/forgot-password — gửi mã đặt lại mật khẩu qua email.

    Backend app LUÔN trả cùng 1 thông báo chung chung (chống user
    enumeration) kể cả khi email không tồn tại — không raise lỗi riêng ở
    đây để giữ đúng hành vi đó."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.post("/auth/forgot-password", json={"email": email})
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json().get("message", "Đã gửi mã xác thực.")


async def confirm_password_reset(token: str, new_password: str) -> str:
    """Proxy POST /auth/reset-password — xác nhận mã + đặt mật khẩu mới."""
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.post(
            "/auth/reset-password",
            json={"token": token, "new_password": new_password, "confirm_password": new_password},
        )
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json().get("message", "Đã đổi mật khẩu.")


def _extract_detail(response: httpx.Response) -> str:
    try:
        return response.json().get("detail", "Đăng nhập thất bại.")
    except ValueError:
        return "Đăng nhập thất bại."
