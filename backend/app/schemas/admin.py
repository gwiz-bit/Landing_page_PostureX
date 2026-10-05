from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WaitlistEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    source: str | None
    created_at: datetime


class WaitlistListOut(BaseModel):
    total: int
    entries: list[WaitlistEntryOut]
