from pydantic import BaseModel, EmailStr
from typing import Optional


class CashierCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str


class CashierUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None


class CashierResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True