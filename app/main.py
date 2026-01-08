from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api import category, keyword, transaction, autocategorize, stats
from app.logging import setup_logging
from app.scheduler import start_scheduler
import logging

setup_logging()

start_scheduler()

app = FastAPI(title="Budget Tracker API")

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(keyword.router, prefix="/keywords", tags=["Keywords"])
app.include_router(transaction.router, prefix="/transactions", tags=["Transactions"])
app.include_router(autocategorize.router, prefix="/categorize", tags=["Categorization"])
app.include_router(stats.router, prefix="/stats", tags=["Statistics"])

logger = logging.getLogger(__name__)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, ex: Exception):
    logger.exception("Unhandled exception", extra={"path": request.url.path, "method": request.method})
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})