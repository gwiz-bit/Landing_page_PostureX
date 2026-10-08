# CLAUDE.md — PostureX Landing Page

Đọc file này TRƯỚC khi làm việc. Sau mỗi lần làm xong việc gì, thêm một dòng vào "Nhật ký công việc" (ngày + nội dung) và cập nhật các mục bên trên nếu thực tế đã đổi.

## Mục tiêu dự án
Landing page cho app PostureX (đồ án EXE202, FPT). Mục tiêu chính: thu hút người xem và thu email đăng ký tải trước (waitlist) để có data người dùng.

## Kiến trúc
- `landing/` — frontend tĩnh (HTML/CSS/JS thuần): `index.html`, `login.html`, `account.html`, `admin-waitlist.html`, `assets/images/`.
- `backend/` — FastAPI, phục vụ luôn `landing/` qua `StaticFiles` (mount `/` phải đặt SAU mọi route khác trong `app/main.py`).
  - `app/api/routes/`: `auth.py` (login/logout/me, `require_admin`), `waitlist.py`, `admin.py`.
  - `app/core/`: `config.py`, `security.py` (session JWT), `database.py` (SQLite), `rate_limit.py`.
  - `app/models/waitlist.py`, `app/schemas/`, `app/services/posturex_client.py`.
  - DB: SQLite tại `backend/data/web.db` (bảng `waitlist_signups`).
- Repo này TÁCH với backend app PostureX (repo khác, mặc định `http://localhost:9000/api/v1`). Web không có bảng Users; đăng nhập gọi sang backend app qua httpx.

## Chạy local
```
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload     # http://localhost:8000
```
Cần `backend/.env` (copy từ `.env.example`, đặt `SECRET_KEY`). Đăng nhập admin cần backend app chạy ở cổng 9000.

## Waitlist — hiện trạng
- `POST /api/waitlist`: lưu `email` + `source`, giới hạn 10 lượt/giờ; email trùng vẫn trả thông báo thành công.
- `GET /api/admin/waitlist`: chỉ admin (cookie session có `is_admin=true`, KHÔNG dùng API key). Trang xem + tải CSV: `/admin-waitlist.html`.
- Chưa có: endpoint đếm công khai (`/count`), checkbox consent, UTM, email xác nhận, test tự động.
- `config.py` còn cấu hình MySQL (`DB_*`, `get_database_url`) nhưng không dùng — thực tế là SQLite.

## Ghi chú / quyết định
- Đăng ký tài khoản + OTP qua web đang TẮT (`REGISTRATION_ENABLED=False`) vì lỗ hổng brute-force OTP bên backend app; chỉ bật lại sau khi backend app vá.
- Cookie session đang `secure=False`; BẬT LẠI khi deploy HTTPS.
- Ngôn ngữ: giao tiếp và comment code bằng tiếng Việt.

## Việc nên làm tiếp (đề xuất)
- Hiệu ứng cho landing (animation khi cuộn, mockup app, social proof).
- Endpoint `/api/waitlist/count`, consent, UTM tracking, rate-limit/honeypot chống bot.
- Viết pytest cho waitlist và admin; script tạo cookie admin giả để test local.

## Nhật ký công việc
Định dạng: `YYYY-MM-DD — nội dung`. Mục mới thêm xuống cuối.

- (trước 2026-10-08, do người dùng tự code; ngày chính xác không được ghi lại) — Backend FastAPI + landing tĩnh, đăng nhập qua backend app, tính năng waitlist (model, route, form trong `index.html`, trang admin `admin-waitlist.html` có xuất CSV), rate-limit. Xem `git log` để biết ngày chính xác (vd commit "Them trang admin xem danh sach email dang ky tai truoc (waitlist)", "thay email support").
- 2026-10-08 — Claude rà soát code, xác nhận waitlist + trang admin đã có, hướng dẫn cách test; tạo file CLAUDE.md này. Chưa sửa code nào khác.
