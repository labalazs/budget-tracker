from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    description: str
    amount: float
    created_at: Optional[datetime] = None
    category_id: Optional[int] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True