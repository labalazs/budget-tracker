from pydantic import BaseModel, ConfigDict

class KeywordBase(BaseModel):
    keyword: str
    category_id: int

class KeywordCreate(KeywordBase):
    pass

class KeywordRead(KeywordBase):
    id: int
    model_config = ConfigDict(from_attributes=True)