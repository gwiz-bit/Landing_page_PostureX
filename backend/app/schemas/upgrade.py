from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class UpgradeIn(BaseModel):
    plan: Literal["pro"]


class UpgradeOut(BaseModel):
    order_id: int
    invoice: str
    amount: int
    # Trình duyệt POST các `fields` (đúng thứ tự) tới `action` để sang trang thanh toán SePay.
    action: str
    fields: dict[str, str]


class OrderStatusOut(BaseModel):
    status: str
    expires_at: datetime | None


class MyPlanOut(BaseModel):
    plan: str  # "Pro" hoặc "Free"
    expires_at: datetime | None


class UpgradeEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    email: str
    full_name: str | None
    plan: str
    amount: int
    transfer_code: str
    status: str
    created_at: datetime
    paid_at: datetime | None
    expires_at: datetime | None
    paid_amount: int | None


class UpgradeListOut(BaseModel):
    total: int
    entries: list[UpgradeEntryOut]


class UpgradeStatusIn(BaseModel):
    status: Literal["paid", "cancelled"]
