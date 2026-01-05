from fastapi import FastAPI
from app.api import category, keyword, transaction, autocategorize, stats

app = FastAPI(title="Budget Tracker API")

app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(keyword.router, prefix="/keywords", tags=["Keywords"])
app.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])
app.include_router(autocategorize.router, prefix="/categorize", tags=["Categorization"])
# app.include_router(stats.router, prefix="/stats", tags=["Statistics"])