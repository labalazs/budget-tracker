from sqlalchemy.orm import Session
from app.models.keyword import CategoryKeyword
from app.models.category import Category

def suggest_category(description: str, db: Session) -> int | None:
    text = description.lower()
    keywords = db.query(CategoryKeyword).join(Category).filter(Category.is_parent == False).all()
    for keyword in keywords:
        if keyword.keyword in text:
            return {
                "category_id": keyword.category_id,
                "category_name": keyword.category.name,
                "reason": f'Matched keyword "{keyword.keyword}"',
            }
    return {
        "category_id": None,
        "category_name": None,
        "reason": "No matching keyword found",
    }