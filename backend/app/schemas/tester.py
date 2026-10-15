from pydantic import BaseModel, EmailStr


class TesterIn(BaseModel):
    email: EmailStr
