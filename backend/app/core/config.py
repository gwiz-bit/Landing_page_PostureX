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
    # Cookie đăng nhập chỉ gửi qua HTTPS (cờ Secure) — tránh bị đánh cắp trên mạng không
    # tin cậy. Mặc định BẬT cho bản chạy thật (https://posturex1.com). Chrome/Edge/Firefox
    # vẫn nhận cookie Secure trên http://localhost; nếu trình duyệt dev nào không nhận
    # (vd Safari) thì đặt COOKIE_SECURE=False trong .env CỦA MÁY ĐÓ, không đổi mặc định.
    COOKIE_SECURE: bool = True
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

    # SePay (tự xác nhận chuyển khoản mua gói). SEPAY_API_KEY là chuỗi bí mật đặt
    # ở cả `.env` này lẫn trang cấu hình webhook của SePay (kiểu xác thực API Key).
    # Để trống = webhook từ chối mọi yêu cầu. SEPAY_ACCOUNT_NUMBER (tuỳ chọn): chỉ
    # nhận giao dịch vào đúng số tài khoản này.
    SEPAY_API_KEY: str = ""
    SEPAY_ACCOUNT_NUMBER: str = ""

    # Cổng thanh toán SePay (my.sepay.vn → Cổng thanh toán). MERCHANT ID + SECRET KEY lấy
    # ở màn hình tích hợp (Sandbox và Production là HAI bộ khác nhau). SECRET KEY dùng để
    # ký form thanh toán VÀ cũng là giá trị header X-Secret-Key mà SePay gửi kèm IPN.
    # Để trống = không tạo được đơn thanh toán. PUBLIC_BASE_URL (tuỳ chọn) là địa chỉ web
    # công khai dùng cho đường dẫn quay về (vd https://posturex.vn); bỏ trống thì lấy từ request.
    SEPAY_PG_MERCHANT_ID: str = ""
    SEPAY_PG_SECRET_KEY: str = ""
    SEPAY_PG_ENV: str = "sandbox"  # "sandbox" hoặc "production"
    PUBLIC_BASE_URL: str = ""

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
