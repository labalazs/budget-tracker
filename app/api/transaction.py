from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import logging

from app.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.services.categorizer import suggest_category
from app.services.learning import learn_from_override

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/", response_model=List[TransactionRead])
def get_transactions(category_id: int | None = None, date_from: datetime | None = None, date_to: datetime | None = None, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if date_from:
        query = query.filter(Transaction.created_at >= date_from)
    if date_to:
        query = query.filter(Transaction.created_at <= date_to)
    return query.all()

@router.get("/{transaction_id}", response_model=TransactionRead)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        logger.warning(f'Transaction (id={transaction_id}) not found')
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    category_id = data.category_id
    if category_id is None:
        category_id = suggest_category(data.description, db)["category_id"]
    if category_id:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category or category.is_parent:
            logger.warning(f'Invalid category_id={category_id}')
            raise HTTPException(status_code=400, detail="Invalid category_id")
    transaction = Transaction(description=data.description, amount=data.amount, category_id=category_id, created_at=data.created_at or datetime.utcnow())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

@router.put("/{transaction_id}", response_model=TransactionRead)
def update_transaction(transaction_id: int, data: TransactionCreate, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        logger.warning(f'Transaction (id={transaction_id}) not found')
        raise HTTPException(status_code=404, detail="Transaction not found")
    old_category_id = transaction.category_id
    if data.category_id:
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if not category or category.is_parent:
            logger.warning(f'Invalid category_id={data.category_id}')
            raise HTTPException(status_code=400, detail="Invalid category_id")
        transaction.category_id = data.category_id
    transaction.description = data.description
    transaction.amount = data.amount
    transaction.created_at = data.created_at
    db.commit()
    db.refresh(transaction)
    if data.category_id and data.category_id != old_category_id:
        learn_from_override(description=transaction.description, category_id=data.category_id, db=db)
    return transaction

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        logger.warning(f'Transaction (id={transaction_id}) not found')
        raise HTTPException(status_code=404, detail="Transaction not found")
    db.delete(transaction)
    db.commit()