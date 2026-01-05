from pydantic import BaseModel

class KeywordBase(BaseModel):
    keyword: str
    category_id: int

class KeywordCreate(KeywordBase):
    pass

class KeywordRead(KeywordBase):
    id: int

    class Config:
        orm_mode = True