from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

_Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]
_Message = Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=2000)]


class FeedbackIn(BaseModel):
    name: _Name
    email: EmailStr
    message: _Message
    # Ô ẩn chống bot (honeypot): người thật không thấy nên không bao giờ điền,
    # bot tự động điền mọi ô nó tìm thấy. Có giá trị → coi là spam.
    website: str | None = None
