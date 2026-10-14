# CLAUDE.md — PostureX Landing Page

Đọc file này TRƯỚC khi làm việc. Sau mỗi lần làm xong việc gì, thêm một dòng vào "Nhật ký công việc" (ngày + nội dung) và cập nhật các mục bên trên nếu thực tế đã đổi.

## Mục tiêu dự án
Landing page cho app PostureX (đồ án EXE202, FPT). Mục tiêu chính: thu hút người xem và thu email đăng ký tải trước (waitlist) để có data người dùng.

## Kiến trúc
- `landing/` — frontend tĩnh (HTML/CSS/JS thuần):
  - `index.html` — landing công khai, **đồng thời là trang "chủ" thật sự sau khi đăng nhập** (không redirect sang trang riêng nào khác). Header tự gọi `GET /api/auth/me` lúc tải trang để đổi link "Đăng nhập" thành icon "Hồ sơ" nếu đã có phiên hợp lệ.
  - `login.html`, `register.html` — đăng ký là wizard 4 bước (tài khoản → OTP → thể chất → ngày tập/mục tiêu), giống `OnboardingFlow` bên app. Xong bước 4 KHÔNG tự đăng nhập vào thẳng app — quay về `index.html`, người dùng tự đăng nhập lại.
  - `account.html` — trang **Hồ sơ**: xem/sửa theo từng mục (icon ✏️ bật form sửa riêng cho từng trường, chỉ hiện trường đã có giá trị), đổi mật khẩu (chỉ cần mật khẩu mới x2, không cần mật khẩu cũ/email — giống `EditProfileScreen` bên app), card "Lịch tập" dẫn sang `workout-plan.html`, card "Quản trị" (chỉ hiện nếu `is_admin=true`) dẫn sang `admin-waitlist.html`.
  - `workout-plan.html` — lịch tập 4 tuần (**tên cũ là `home.html`, đã đổi** vì nó không phải trang chủ). Sửa được từng ngày tại chỗ (đổi tên buổi/thêm-bớt-sửa bài tập), giống `_DayDetailSheet` bên app.
  - `admin-waitlist.html` — chỉ admin, xem + xuất CSV danh sách waitlist.
  - `assets/js/onboarding-options.js`, `assets/js/workout-plan.js` — **port 1:1 từ `lib/models/onboarding_options.dart`/`workout_plan.dart` bên repo app**. Đổi logic bên app thì nhớ đổi cả 2 file JS này, không tự động đồng bộ.
  - `assets/images/`.
- `backend/` — FastAPI, phục vụ luôn `landing/` qua `StaticFiles` (mount `/` phải đặt SAU mọi route khác trong `app/main.py`).
  - `app/api/routes/`: `auth.py` (register/verify-otp/resend-otp/login/logout/me, `require_login`, `require_admin`), `waitlist.py`, `admin.py`, `profile.py` (mới — `GET/PUT /api/profile`, `PATCH /api/account`, `GET /api/exercises`, đều proxy sang backend app).
  - `app/core/`: `config.py`, `security.py` (session JWT — **giờ nhúng thêm `backend_access_token`** của backend app vào payload, để các route proxy dùng lại không cần đăng nhập lại lần nữa), `database.py` (SQLite), `rate_limit.py`.
  - `app/models/waitlist.py`, `app/schemas/` (`admin.py`, `auth.py`, `profile.py`), `app/services/posturex_client.py` (mọi hàm gọi sang backend app).
  - DB: SQLite tại `backend/data/web.db` (bảng `waitlist_signups`).
- Repo này TÁCH với backend app PostureX (repo khác, mặc định `http://localhost:9000/api/v1`). Web không có bảng Users; mọi thao tác tài khoản (đăng ký/OTP/đăng nhập/sửa hồ sơ/đổi mật khẩu) đều proxy sang backend app qua httpx.

### Lịch tập lưu ở đâu — đọc kỹ trước khi đụng vào
Chỉ 5 trường có cột thật ở backend app (`gender`/`age`/`height_cm`/`weight_kg`/
`fitness_level`/`weekly_goal`) — các trường còn lại của lịch tập (ngày tập,
nhóm cơ trọng tâm, thiết bị, mục tiêu, vấn đề sức khoẻ) **không có cột backend
nào cả**, kể cả bên app. Web dùng `localStorage` (key `"posturex_plan"`, có
`email`, `startDate`, `days`, `criteria`) để giữ lại — khớp đúng cách
`TokenStorage.savePlanParams()`/`readPlanParams()` bên app lưu cục bộ trên
thiết bị. Vài điểm dễ quên:
- Chỉ đáng tin trên **cùng trình duyệt/máy** đã đăng ký — đăng nhập ở máy khác
  sẽ không thấy, tự sinh lịch mặc định từ 5 trường backend (không lỗi, chỉ
  không đúng ý người dùng đã chọn).
- Sửa "Buổi tập/tuần"/"Trình độ" trong Hồ sơ → `account.html` tự sinh lại
  lịch cache (nếu có) bằng `generateWorkoutPlan()`, giữ nguyên `criteria` gốc.
- Sửa tay 1 ngày trong `workout-plan.html` → ghi đè `localStorage` luôn, kể cả
  khi trước đó chưa có cache nào (tạo mới với `criteria` rỗng) — giống
  `TokenStorage.saveAiPlanDays()` bên app.
- Đăng xuất **KHÔNG xoá** `"posturex_plan"` — cố ý, khớp
  `TokenStorage.clearSession()` bên app (giữ lại qua logout).

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
- ⚠️ **`REGISTRATION_ENABLED=True` từ 14/10/2026** — BẬT LẠI có chủ đích để
  làm tính năng đăng ký đầy đủ, CHẤP NHẬN RỦI RO TẠM THỜI dù lỗ hổng gốc
  (`/auth/verify-otp` không giới hạn số lần thử OTP, `/auth/register` không
  ép độ mạnh mật khẩu) bên backend app **đã được vá một phần** (rate-limit đã
  thêm, xem commit `050c474` bên repo app) — kiểm tra lại thật kỹ trước khi
  coi đây là an toàn tuyệt đối.
- Cookie session đang `secure=False`; BẬT LẠI khi deploy HTTPS.
- OTP đăng ký khi **SMTP chưa cấu hình** (máy local chưa điền `SMTP_USER`
  thật bên `backend/.env` của repo app) sẽ KHÔNG gửi email — backend app tự
  in mã ra log dạng `[DEV] SMTP chưa cấu hình — OTP cho <email> là: <mã>`.
  Tìm dòng đó trong console đang chạy `uvicorn`/`run.ps1` để lấy mã lúc test
  local. Trên VPS production, SMTP đã cấu hình thật từ trước (app mobile
  vẫn đang gửi OTP email thật) — không cần làm gì thêm khi deploy.
- Ngôn ngữ: giao tiếp và comment code bằng tiếng Việt.

## Việc nên làm tiếp (đề xuất)
- Hiệu ứng cho landing (animation khi cuộn, mockup app, social proof).
- Endpoint `/api/waitlist/count`, consent, UTM tracking, rate-limit/honeypot chống bot.
- Viết pytest cho waitlist và admin; script tạo cookie admin giả để test local.

## Nhật ký công việc
Định dạng: `YYYY-MM-DD — nội dung`. Mục mới thêm xuống cuối.

- (trước 2026-10-08, do người dùng tự code; ngày chính xác không được ghi lại) — Backend FastAPI + landing tĩnh, đăng nhập qua backend app, tính năng waitlist (model, route, form trong `index.html`, trang admin `admin-waitlist.html` có xuất CSV), rate-limit. Xem `git log` để biết ngày chính xác (vd commit "Them trang admin xem danh sach email dang ky tai truoc (waitlist)", "thay email support").
- 2026-10-08 — Claude rà soát code, xác nhận waitlist + trang admin đã có, hướng dẫn cách test; tạo file CLAUDE.md này. Chưa sửa code nào khác.
- 2026-10-14 — **Đăng ký đầy đủ như app + Hồ sơ + Lịch tập sửa tay.** Thay đổi
  lớn, đọc kỹ mục "Lịch tập lưu ở đâu" ở trên trước khi đụng vào các trang
  dưới đây:
  - **`register.html`** viết lại thành wizard 4 bước (tài khoản → OTP → thể
    chất → ngày tập/mục tiêu), sinh lịch tập bằng `generateWorkoutPlan()`
    (port từ `workout_plan.dart`) ngay sau bước 4, lưu vào `localStorage`
    kèm `criteria` gốc, rồi về `index.html` — KHÔNG tự đăng nhập thẳng vào
    trang lịch tập.
  - **`home.html` đổi tên thành `workout-plan.html`** — không còn là trang
    chủ, chỉ truy cập từ Hồ sơ. `login.html` (đã sửa lỗi quên — trước đó vẫn
    trỏ nhầm "home.html" cũ gây 404) và mọi nơi khác đều về `index.html` sau
    đăng nhập/đăng ký, không phải trang lịch tập.
  - **`index.html`** — header session-aware (tự check `/api/auth/me`), hiện
    icon "Hồ sơ" thay "Đăng nhập" nếu đã có phiên — tránh cảm giác "bị
    logout" khi quay lại trang này từ trang khác.
  - **`account.html` (Hồ sơ) viết lại hoàn toàn** — view-mode mặc định, mỗi
    trường có icon ✏️ sửa riêng, chỉ hiện trường thể chất đã có giá trị (nút
    "+ Thêm thông tin còn thiếu" cho trường trống), đổi mật khẩu gộp vào
    "Thông tin tài khoản" (hiện `••••••••`, sửa chỉ cần mật khẩu mới x2 —
    ĐÃ THỬ cách gửi OTP qua email trước, sau đó bỏ vì app không làm vậy),
    card "Lịch tập" + card "Quản trị" (chỉ `is_admin=true`).
  - **`workout-plan.html`** thêm sửa tay từng ngày (icon ✏️ → đổi tên buổi
    tập + thêm/bớt/sửa bài tập, giống `_DayDetailSheet` bên app) — lưu đè
    `localStorage` ngay cả khi trước đó chưa có cache.
  - **2 lỗi CSS nhãn đè lên ô nhập** đã sửa — một ở `account.html` (nhãn nằm
    ngoài `.edit-row` nên không có CSS nào áp dụng), một ở `register.html`
    **chưa ai báo nhưng đã tồn tại từ trước** (`label:first-of-type` khớp
    nhầm cả 2 nhãn trong mỗi hàng `.row-2`, không chỉ nhãn đầu form — sửa
    bằng cách để `.row-2` tự giữ `margin-top`, không dựa thứ tự DOM nữa).
  - Backend: `security.py` nhúng `backend_access_token` vào session JWT;
    route mới `app/api/routes/profile.py` + `app/schemas/profile.py`; thêm
    rồi XOÁ lại 2 route `forgot-password`/`reset-password` proxy (thử cách
    đổi mật khẩu qua email trước, sau đó bỏ để khớp đúng app — không còn
    dead code nào sót lại).
  - ⚠️ Chưa test qua trình duyệt thật (môi trường làm việc không có công cụ
    trình duyệt) — mọi xác nhận đều qua `curl` (luồng API) + Node
    (`new Function()` syntax-check, mô phỏng `generateWorkoutPlan()` bằng
    tay). Cần người thật bấm thử trọn luồng đăng ký → sửa hồ sơ → sửa lịch
    tập → đăng xuất → đăng nhập lại trước khi coi là ổn định.
