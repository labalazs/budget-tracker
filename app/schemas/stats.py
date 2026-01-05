from pydantic import BaseModel
from typing import List

class CategoryStat(BaseModel):
    category: str
    total_amount: float

class MonthlyStat(BaseModel):
    month: str
    category: str
    total_amount: float

class StatsResponse(BaseModel):
    by_category: List[CategoryStat]
    monthly_totals: List[MonthlyStat]