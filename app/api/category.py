from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryRead

router = APIRouter()

def build_category_tree(categories: List[Category]) -> List[Category]:
    roots = []
    for cat in categories:
        if not cat.is_parent and cat.parent_id:
            continue
        else:
            roots.append(cat)
    return roots

@router.get("/", response_model=List[CategoryRead])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    tree = build_category_tree(categories)
    return tree

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    if data.is_parent and data.parent_id is not None:
        raise HTTPException(status_code=400, detail="Parent category cannot have parent_id")
    if not data.is_parent:
        if data.parent_id is None:
            raise HTTPException(status_code=400, detail="Child category must have a parent_id")
        parent = db.query(Category).filter(Category.id == data.parent_id).first()
        if not parent or not parent.is_parent:
            raise HTTPException(status_code=400, detail="parent_id must refer to a parent category")
    category = Category(name=data.name, is_parent=data.is_parent, parent_id=data.parent_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = data.name
    category.is_parent = data.is_parent
    category.parent_id = data.parent_id
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()