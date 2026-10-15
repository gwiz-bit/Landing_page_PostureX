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


class TesterEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    created_at: datetime


class TesterListOut(BaseModel):
    total: int
    entries: list[TesterEntryOut]


class FeedbackEntryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    message: str
    created_at: datetime


class FeedbackListOut(BaseModel):
    total: int
    entries: list[FeedbackEntryOut]
