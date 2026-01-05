from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.schemas.stats import StatsResponse
from app.services.stats import get_stats

router = APIRouter()

@router.get("/", response_model=StatsResponse)
def stats(date_from: datetime | None = None, date_to: datetime | None = None, db: Session = Depends(get_db)):
    by_parent, monthly = get_stats(db=db, date_from=date_from, date_to=date_to)
    return {
        "by_category": by_parent,
        "monthly_totals": monthly,
    }