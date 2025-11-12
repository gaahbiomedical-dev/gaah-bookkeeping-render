from pydantic import BaseModel
from typing import Optional
import datetime

class TransactionCreate(BaseModel):
    date: Optional[datetime.date] = None
    item: str
    quantity: float
    rate: float
    total: Optional[float] = None
    patient: Optional[str] = None
    department: Optional[str] = None
    book_name: Optional[str] = 'Default'

class TransactionOut(TransactionCreate):
    id: int
    entered_by: Optional[str]
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = 'user'

class Token(BaseModel):
    access_token: str
    token_type: str
