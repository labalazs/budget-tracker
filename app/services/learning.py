import logging
from sqlalchemy.orm import Session

from app.models.keyword import CategoryKeyword
from app.models.category import Category

logger = logging.getLogger(__name__)

def extract_candidate_keyword(description: str) -> str | None:
    words = description.lower().split()
    for word in words:
        if len(word) < 4:
            continue
        if not word.isalpha():
            continue
        return word
    return None

def learn_from_override(description: str, category_id: int, db: Session):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category or category.is_parent:
        logger.warning(f'Learning skipped: invalid category (id={category_id})')
        return
    keyword = extract_candidate_keyword(description=description)
    if not keyword:
        logger.info(f'Could not extract suitable keyword from: "{description}"')
        return
    exists = (db.query(CategoryKeyword).filter(CategoryKeyword.category_id == category_id, CategoryKeyword.keyword == keyword).first())
    if exists:
        logger.info(f'Keyword "{keyword}" already exists')
        return
    db.add(CategoryKeyword(keyword=keyword, category_id=category_id))
    db.commit()
    logger.info(f'Learned new keyword "{keyword}" for category (id={category_id})')
