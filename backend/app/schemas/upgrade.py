from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class UpgradeIn(BaseModel):
    plan: Literal["pro"]


class UpgradeOut(BaseModel):
    message: str
    transfer_code: str
    amount: int


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


class UpgradeListOut(BaseModel):
    total: int
    entries: list[UpgradeEntryOut]


class UpgradeStatusIn(BaseModel):
    status: Literal["approved", "rejected"]
