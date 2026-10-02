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


async def verify_otp_and_fetch_profile(email: str, otp_code: str) -> dict:
    """Xác thực OTP vừa đăng ký — /auth/verify-otp trả access_token luôn
    (kiêm đăng nhập lần đầu), rồi gọi tiếp /users/me như login thường."""
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
        return me_resp.json()


async def resend_otp(email: str) -> str:
    async with httpx.AsyncClient(base_url=settings.POSTUREX_API_BASE_URL, timeout=20.0) as client:
        resp = await client.post("/auth/resend-otp", json={"email": email})
        if resp.status_code != 200:
            raise PostureXAuthError(resp.status_code, _extract_detail(resp))
        return resp.json().get("message", "Đã gửi lại mã OTP.")


async def login_and_fetch_profile(email: str, password: str) -> dict:
    """Đăng nhập bằng /auth/login rồi lấy thông tin qua /users/me.

    Hai lời gọi tuần tự vì /auth/login chỉ trả về access_token, không kèm
    tên/email/sđt (xem backend/app/schemas/auth.py::TokenResponse của repo
    app) — đúng thiết kế hiện tại của backend app, không phải thiếu sót.
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

        return me_resp.json()


def _extract_detail(response: httpx.Response) -> str:
    try:
        return response.json().get("detail", "Đăng nhập thất bại.")
    except ValueError:
        return "Đăng nhập thất bại."
