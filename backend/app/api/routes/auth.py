"""Đăng nhập/đăng ký trên web bằng đúng tài khoản dùng chung với app PostureX.

Web không có bảng Users riêng — mọi thao tác tài khoản (đăng ký, xác thực
OTP, đăng nhập) đều proxy sang backend app, xem services/posturex_client.py.
Tài khoản tạo ở đây dùng đăng nhập được luôn trên app mobile và ngược lại."""

from fastapi import APIRouter, HTTPException, Response
from fastapi import Request as FastAPIRequest

from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import create_session_token, decode_session_token
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    ResendOtpRequest,
    UserProfileOut,
    VerifyOtpRequest,
)
from app.services.posturex_client import (
    PostureXAuthError,
    login_and_fetch_profile,
    register as register_user,
    resend_otp as resend_otp_code,
    verify_otp_and_fetch_profile,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

_REGISTRATION_DISABLED_MESSAGE = (
    "Đăng ký trên web đang tạm khoá. Vui lòng đăng ký trên app PostureX."
)


def _require_registration_enabled() -> None:
    if not settings.REGISTRATION_ENABLED:
        raise HTTPException(status_code=503, detail=_REGISTRATION_DISABLED_MESSAGE)


def _set_session_cookie(response: Response, profile: dict) -> None:
    token = create_session_token(
        user_id=profile["id"],
        email=profile["email"],
        full_name=profile.get("full_name"),
        phone_number=profile.get("phone_number"),
    )
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=settings.SESSION_EXPIRE_MINUTES * 60,
        # secure=True bị tắt vì chưa có HTTPS lúc code — BẬT LẠI khi deploy
        # thật lên domain có SSL.
        secure=False,
    )


@router.post("/register", response_model=MessageResponse)
@limiter.limit("5/hour")
async def register(request: FastAPIRequest, data: RegisterRequest) -> MessageResponse:
    _require_registration_enabled()
    try:
        await register_user(data.email, data.password, data.full_name)
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return MessageResponse(
        message="Đã gửi mã OTP xác thực tới email. Vui lòng kiểm tra hộp thư."
    )


@router.post("/verify-otp", response_model=UserProfileOut)
@limiter.limit("10/minute")
async def verify_otp(
    request: FastAPIRequest, data: VerifyOtpRequest, response: Response
) -> UserProfileOut:
    _require_registration_enabled()
    try:
        profile = await verify_otp_and_fetch_profile(data.email, data.otp_code)
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    _set_session_cookie(response, profile)
    return UserProfileOut(**profile)


@router.post("/resend-otp", response_model=MessageResponse)
@limiter.limit("5/hour")
async def resend_otp_endpoint(request: FastAPIRequest, data: ResendOtpRequest) -> MessageResponse:
    _require_registration_enabled()
    try:
        message = await resend_otp_code(data.email)
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return MessageResponse(message=message)


@router.post("/login", response_model=UserProfileOut)
@limiter.limit("10/minute;100/hour")
async def login(request: FastAPIRequest, data: LoginRequest, response: Response) -> UserProfileOut:
    try:
        profile = await login_and_fetch_profile(data.email, data.password)
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    _set_session_cookie(response, profile)
    return UserProfileOut(**profile)


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return {"message": "Đã đăng xuất."}


@router.get("/me", response_model=UserProfileOut)
async def me(request: FastAPIRequest) -> UserProfileOut:
    token = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Chưa đăng nhập.")
    payload = decode_session_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Phiên đăng nhập đã hết hạn.")
    return UserProfileOut(
        id=int(payload["sub"]),
        email=payload["email"],
        full_name=payload.get("full_name"),
        phone_number=payload.get("phone_number"),
    )
