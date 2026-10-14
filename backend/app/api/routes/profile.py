"""Hồ sơ thể chất + danh sách bài tập — proxy sang backend app, dùng cho
trang Hồ sơ (`account.html`) và trang sinh lịch tập (`home.html`,
`register.html` bước 4).

Mọi route ở đây (trừ `/api/exercises`) cần đăng nhập — lấy
`backend_access_token` từ payload JWT của session cookie (xem
`routes/auth.py::require_login`) rồi forward sang backend app, KHÔNG tự
gọi lại /auth/login."""

from fastapi import APIRouter, Depends, HTTPException

from app.api.routes.auth import require_login
from app.schemas.profile import AccountUpdate, ProfileOut, ProfileUpdate
from app.services.posturex_client import (
    PostureXAuthError,
    get_profile as fetch_profile,
    list_exercises as fetch_exercises,
    update_account as patch_account,
    update_profile as put_profile,
)

router = APIRouter(prefix="/api", tags=["profile"])


@router.get("/profile", response_model=ProfileOut)
async def get_profile(payload: dict = Depends(require_login)) -> ProfileOut:
    try:
        data = await fetch_profile(payload["backend_access_token"])
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return ProfileOut(**data)


@router.put("/profile", response_model=ProfileOut)
async def update_profile(
    data: ProfileUpdate, payload: dict = Depends(require_login)
) -> ProfileOut:
    try:
        result = await put_profile(
            payload["backend_access_token"], data.model_dump(exclude_none=True)
        )
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return ProfileOut(**result)


@router.patch("/account")
async def update_account(
    data: AccountUpdate, payload: dict = Depends(require_login)
) -> dict:
    try:
        result = await patch_account(
            payload["backend_access_token"], data.model_dump(exclude_none=True)
        )
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    return result


@router.get("/exercises")
async def list_exercises() -> list[dict]:
    """Không cần đăng nhập — đúng với endpoint gốc phía backend app."""
    try:
        return await fetch_exercises()
    except PostureXAuthError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
