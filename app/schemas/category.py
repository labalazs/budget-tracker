from typing import Optional, List
from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    is_parent: bool = False
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    children: List["CategoryRead"] = []

    class Config:
        orm_mode = True

CategoryRead.update_forward_refs()