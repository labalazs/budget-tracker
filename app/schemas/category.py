from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    name: str
    is_parent: bool = False
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    children: List["CategoryRead"] = []
    model_config = ConfigDict(from_attributes=True)

CategoryRead.model_rebuild()