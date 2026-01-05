from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.models.keyword import CategoryKeyword
from app.models.category import Category
from app.schemas.keyword import KeywordCreate, KeywordRead

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[KeywordRead])
def get_keywords(category_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(CategoryKeyword)
    if category_id:
        query = query.filter(CategoryKeyword.category_id == category_id)
    return query.all()

@router.post("/", response_model=KeywordRead, status_code=status.HTTP_201_CREATED)
def create_keyword(data: KeywordCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == data.category_id).first()
    if not category:
        logger.warning(f'Category (id={data.category_id}) not found')
        raise HTTPException(status_code=404, detail="Category not found")
    if category.is_parent:
        logger.warning(f'Cannot assign keywords to parent categories')
        raise HTTPException(status_code=400, detail="Cannot assign keywords to parent categories")
    existing = (db.query(CategoryKeyword).filter(CategoryKeyword.category_id == data.category_id, CategoryKeyword.keyword == data.keyword.lower()).first())
    if existing:
        logger.warning(f'Keyword already exists for this category')
        raise HTTPException(status_code=400, detail="Keyword already exists for this category")
    keyword = CategoryKeyword(keyword=data.keyword.lower(), category_id=data.category_id)
    db.add(keyword)
    db.commit()
    db.refresh(keyword)
    return keyword

@router.delete("/{keyword_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_keyword(keyword_id: int, db: Session = Depends(get_db)):
    keyword = db.query(CategoryKeyword).filter(CategoryKeyword.id == keyword_id).first()
    if not keyword:
        logger.warning(f'Keyword (id={keyword_id}) not found')
        raise HTTPException(status_code=404, detail="Keyword not found")
    db.delete(keyword)
    db.commit()