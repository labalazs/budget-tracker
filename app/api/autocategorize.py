from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.autocategorize import AutocategorizeRequest, AutocategorizeResponse
from app.services.categorizer import suggest_category

router = APIRouter()

@router.post("/", response_model=AutocategorizeResponse)
def auto_categorize(data: AutocategorizeRequest, db: Session = Depends(get_db)):
    return suggest_category(data.description, db)
    