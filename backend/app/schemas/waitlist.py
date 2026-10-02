from pydantic import BaseModel, EmailStr


class WaitlistIn(BaseModel):
    email: EmailStr
    source: str | None = None


class MessageResponse(BaseModel):
    message: str
