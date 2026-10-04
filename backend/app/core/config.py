"""Cấu hình đọc từ file .env — xem .env.example."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "PostureX Web"
    DEBUG: bool = False

    # Backend chính của app PostureX (repo khác) — web KHÔNG có bảng Users
    # riêng, mọi lần đăng nhập đều hỏi lại backend này qua HTTP server-to-
    # server (không phải browser gọi thẳng, nên không cần CORS ở phía đó).
    POSTUREX_API_BASE_URL: str = "http://localhost:9000/api/v1"

    # Ký session cookie của web (khác hẳn SECRET_KEY của backend app — token
    # JWT của app KHÔNG được dùng lại làm session web, vì hai hệ thống có
    # phạm vi truy cập khác nhau).
    SECRET_KEY: str
    SESSION_COOKIE_NAME: str = "posturex_web_session"
    SESSION_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 ngày, khớp thời hạn token app

    # Tắt TẠM THỜI sau audit bảo mật (xem lịch sử trò chuyện/commit) — đăng
    # ký qua web + OTP không giới hạn số lần thử ở backend app tạo lỗ hổng
    # chiếm tài khoản (đăng ký trước email người khác rồi brute-force OTP,
    # 1 triệu mã, backend app không chặn). Web đã thêm rate limit riêng
    # (10 lần/phút cho verify-otp) giảm rủi ro nhưng KHÔNG loại bỏ hẳn, nên
    # tắt hẳn 3 route đăng ký/OTP cho tới khi backend app vá đúng gốc (thêm
    # giới hạn số lần thử OTP + validate độ mạnh mật khẩu ở UserCreate).
    # Bật lại bằng cách đổi thành True trong .env, không cần đổi code.
    REGISTRATION_ENABLED: bool = False

    # DB riêng của web — chỉ chứa SupportTickets/Vouchers, KHÔNG có bảng Users.
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "posturex_web"
    DB_USER: str = "root"
    DB_PASSWORD: str = ""

    def get_database_url(self) -> str:
        import urllib.parse

        user = urllib.parse.quote_plus(self.DB_USER)
        password = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"mysql+aiomysql://{user}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
