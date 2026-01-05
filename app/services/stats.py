from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from datetime import datetime
import logging

from app.models.transaction import Transaction
from app.models.category import Category

logger = logging.getLogger(__name__)

def get_stats(db: Session, date_from: datetime | None = None, date_to: datetime | None = None):
    logger.info("Preparing statistics")
    query = (db.query(Category.name.label("category"), func.sum(Transaction.amount).label("total")).join(Category, Transaction.category_id == Category.id).group_by(Category.name))
    if date_from:
        query = query.filter(Transaction.created_at >= date_from)
    if date_to:
        query = query.filter(Transaction.created_at <= date_to)
    by_parent = [
        {
            "category": row.category,
            "total_amount": row.total,
        }
        for row in query.all()
    ]
    parent = aliased(Category)
    monthly_query = (db.query(func.strftime("%Y-%m", Transaction.created_at).label("month"), parent.name.label("category"), func.sum(Transaction.amount).label("total")).join(Category, Transaction.category_id == Category.id).join(parent, parent.id == Category.parent_id).group_by("month").group_by("category").order_by("month").order_by("category"))
    if date_from:
        monthly_query = monthly_query.filter(Transaction.created_at >= date_from)
    if date_to:
        monthly_query = monthly_query.filter(Transaction.created_at <= date_to)
    monthly = [
        {
            "month": row.month,
            "category": row.category,
            "total_amount": row.total,
        }
        for row in monthly_query.all()
    ]
    logger.info("Statistics prepared")
    return by_parent, monthly