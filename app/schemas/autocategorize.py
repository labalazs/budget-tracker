from typing import Optional
from pydantic import BaseModel

class AutocategorizeRequest(BaseModel):
    description: str

class AutocategorizeResponse(BaseModel):
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    reason: Optional[str] = None