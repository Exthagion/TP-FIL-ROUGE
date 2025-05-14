from pydantic import BaseModel, EmailStr
from typing import Optional

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        orm_mode = True
